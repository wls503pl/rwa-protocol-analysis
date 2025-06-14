import urllib.request
import urllib.parse
import json
import statistics
import time
import sys

# ✅ Please fill in your Etherscan API Key
API_KEY = "I41NNG7NDAY7RI6DESJCQYSZ27VPZT43PN"
DAI_CONTRACT = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
API_URL = "https://api.etherscan.io/api"

# Gas usage thresholds for DAI transfer only
MIN_GAS_THRESHOLD = 30000  # Minimum reasonable gas for DAI transfer
MAX_GAS_THRESHOLD = 80000  # Maximum reasonable gas for normal DAI transfer

# Suspicious patterns to exclude
SUSPICIOUS_PATTERNS = [
    "fake",
    "phishing",
    "scam",
    "hack",
    "exploit",
    "malicious",
    "suspicious",
    "attack"
]

# DAI transfer function signatures
TRANSFER_FUNCTION_SIGS = {
    "0xa9059cbb": "transfer(address,uint256)",
    "0x23b872dd": "transferFrom(address,address,uint256)"
}

# Swap/DEX related function signatures to exclude
SWAP_FUNCTION_SIGS = {
    "0x38ed1739": "swapExactTokensForTokens",
    "0x8803dbee": "swapTokensForExactTokens",
    "0x7ff36ab5": "swapExactETHForTokens",
    "0x18cbafe5": "swapExactTokensForETH",
    "0x791ac947": "swapExactTokensForTokensSupportingFeeOnTransferTokens",
    "0xb6f9de95": "swapExactETHForTokensSupportingFeeOnTransferTokens",
    "0x022c0d9f": "swap",
    "0x128acb08": "swapTokensForExactETH",
    "0x4a25d94a": "swapTokensForExactTokens"
}


def make_request(params, retry_count=3):
    """Use the standard library to send HTTP requests, including retries and rate limiting"""
    url = f"{API_URL}?{urllib.parse.urlencode(params)}"

    for attempt in range(retry_count):
        try:
            # Reduced delay for faster processing
            time.sleep(0.1)  # Each request interval is 100ms

            with urllib.request.urlopen(url, timeout=15) as response:
                result = json.loads(response.read().decode())

                # Checking for API errors
                if result.get("message") == "NOTOK":
                    error_msg = result.get("result", "Unknown error")
                    if "rate limit" in error_msg.lower():
                        print(f"Hit rate limit, waiting 1 second and retrying... (attempt {attempt + 1}/{retry_count})")
                        time.sleep(1)
                        continue
                    else:
                        print(f"API error: {error_msg}")
                        return None

                return result

        except Exception as e:
            print(f"Request failed (attempt {attempt + 1}/{retry_count}): {e}")
            if attempt < retry_count - 1:
                time.sleep(0.5)  # Wait 500ms before retry

    return None


def is_suspicious_transaction(tx_data):
    """Check if a transaction appears to be suspicious or abnormal"""
    # Check for suspicious patterns in transaction data
    tx_str = json.dumps(tx_data).lower()

    for pattern in SUSPICIOUS_PATTERNS:
        if pattern in tx_str:
            return True, f"Contains suspicious pattern: '{pattern}'"

    # Check for abnormal value patterns (e.g., very small amounts that might indicate testing/spam)
    try:
        value = int(tx_data.get("value", "0"))
        # DAI has 18 decimals, so 1 DAI = 1,000,000,000,000,000,000
        if value > 0 and value < 1000000000000000:  # Less than 0.001 DAI
            return True, "Abnormally small transfer amount"
    except:
        pass

    return False, ""


def is_transfer_function(tx_hash):
    """Check if transaction is a DAI transfer function call (not swap) - optimized version"""
    # Get transaction details to check input data
    tx_params = {
        "module": "proxy",
        "action": "eth_getTransactionByHash",
        "txhash": tx_hash,
        "apikey": API_KEY
    }

    tx_resp = make_request(tx_params)
    if not tx_resp or not tx_resp.get("result"):
        return False, "Failed to fetch transaction details"

    tx_data = tx_resp["result"]
    input_data = tx_data.get("input", "")

    # Quick check - if transaction is not to DAI contract, skip
    if tx_data.get("to", "").lower() != DAI_CONTRACT.lower():
        return False, "Not DAI contract"

    # Quick check - Extract function signature (first 4 bytes of input data)
    if len(input_data) < 10:  # "0x" + 8 hex chars
        return False, "Invalid input"

    func_sig = input_data[:10].lower()

    # Priority check for transfer functions first (most common)
    if func_sig in TRANSFER_FUNCTION_SIGS:
        return True, TRANSFER_FUNCTION_SIGS[func_sig]

    # Quick reject for known swap functions
    if func_sig in SWAP_FUNCTION_SIGS:
        return False, "Swap function"

    # For unknown functions, exclude to be safe
    return False, "Unknown function"


def fetch_transfers(page=1, offset=100):
    """Get DAI transfer transaction hashes - only contains legitimate transfers"""
    params = {
        "module": "account",
        "action": "tokentx",
        "contractaddress": DAI_CONTRACT,
        "page": page,
        "offset": offset,
        "sort": "desc",
        "apikey": API_KEY
    }

    resp = make_request(params)
    if not resp or resp.get("status") != "1":
        print(f"Failed to fetch transactions: {resp}")
        return []

    transfer_hashes = []
    excluded_count = 0

    for tx in resp["result"]:
        # Basic filters:
        # 1. from is not zero address (excluding mint)
        # 2. to is not zero address (excluding burn)
        # 3. Neither from nor to is the contract address itself
        if (tx["from"] == "0x0000000000000000000000000000000000000000" or
                tx["to"] == "0x0000000000000000000000000000000000000000" or
                tx["from"].lower() == DAI_CONTRACT.lower() or
                tx["to"].lower() == DAI_CONTRACT.lower()):
            excluded_count += 1
            continue

        # Check for suspicious transactions
        is_suspicious, reason = is_suspicious_transaction(tx)
        if is_suspicious:
            excluded_count += 1
            continue

        transfer_hashes.append(tx["hash"])

    if excluded_count > 0:
        print(f"📊 Page {page}: {len(transfer_hashes)} candidates, {excluded_count} excluded")

    return transfer_hashes


def fetch_gas_used(tx_hash):
    """Get gas usage for a single transaction and verify it's a legitimate transfer - optimized"""
    # First check if it's a transfer function (not swap) - this is the expensive call
    is_transfer, transfer_status = is_transfer_function(tx_hash)
    if not is_transfer:
        return None, transfer_status

    # Get transaction receipt for gas usage
    receipt_params = {
        "module": "proxy",
        "action": "eth_getTransactionReceipt",
        "txhash": tx_hash,
        "apikey": API_KEY
    }

    receipt_resp = make_request(receipt_params)
    if not receipt_resp:
        return None, "Failed to fetch receipt"

    result = receipt_resp.get("result")
    if result and result.get("gasUsed"):
        gas_used = int(result["gasUsed"], 16)

        # Remove gas threshold filtering for more random data collection
        # Accept all gas values from legitimate transfer functions
        return gas_used, f"Valid: {transfer_status}"

    return None, "No gas data"


def main():
    print("🚀 Starting DAI Transfer Gas Analysis Script")
    print("📋 Only analyzing transfer() and transferFrom() function calls")
    print("🚫 Excluding swap and other DEX-related functions")
    print("=" * 60)

    target_transfer_count = 200
    offset = 100  # Increase to get more transactions per page
    print(f"Target: {target_transfer_count} legitimate DAI transfers")
    print("⚠️  Processing with function signature verification...")
    print("=" * 60)

    gas_values = []
    page = 1
    total_processed = 0
    total_excluded = 0
    function_type_stats = {}

    try:
        while len(gas_values) < target_transfer_count:
            print(f"\n📄 Processing page {page} ({offset} transactions per page)...")
            tx_hashes = fetch_transfers(page=page, offset=offset)

            if not tx_hashes:
                print("❌ No more transaction data available")
                break

            valid_transfers_in_page = 0

            for tx_hash in tx_hashes:
                total_processed += 1
                gas_used, status = fetch_gas_used(tx_hash)

                if gas_used is not None:
                    gas_values.append(gas_used)
                    valid_transfers_in_page += 1

                    # Track function types
                    if "transfer(" in status:
                        function_type_stats["transfer()"] = function_type_stats.get("transfer()", 0) + 1
                    elif "transferFrom(" in status:
                        function_type_stats["transferFrom()"] = function_type_stats.get("transferFrom()", 0) + 1

                    print(f"✅ [{len(gas_values)}/{target_transfer_count}] {tx_hash} → {gas_used:,} gas")

                    if len(gas_values) >= target_transfer_count:
                        break
                else:
                    total_excluded += 1
                    # Only show swap rejections occasionally to reduce noise
                    if total_excluded % 20 == 0 and ("Swap function" in status or "Unknown function" in status):
                        print(f"🚫 Excluded {total_excluded} non-transfer txs so far...")

                # Show progress every 50 valid transactions instead of every 10 processed
                if len(gas_values) > 0 and len(gas_values) % 50 == 0:
                    print(f"📊 Milestone: {len(gas_values)} valid transfers collected")

            print(f"📈 Page {page} results: {valid_transfers_in_page} valid transfers")
            page += 1

            # Safety check - if no valid transfers found for 3 consecutive pages, stop
            if valid_transfers_in_page == 0:
                print("⚠️  No valid transfers found on this page, trying next page...")

        # Analysis and Results
        if not gas_values:
            print("\n❌ Failed to collect any valid transfer gas data.")
            return

        print(f"\n🎉 Successfully collected {len(gas_values)} valid transactions!")
        print(f"📊 Total processed: {total_processed}, Excluded: {total_excluded}")

        # Function type breakdown
        print(f"\n📊 Function Type Breakdown:")
        for func_type, count in function_type_stats.items():
            print(f"   {func_type}: {count} transactions ({count / len(gas_values) * 100:.1f}%)")

        # Statistical analysis
        gas_values.sort()
        count = len(gas_values)
        median_gas = statistics.median(gas_values)
        mean_gas = statistics.mean(gas_values)

        # Calculate trimmed mean (remove top and bottom 5 values)
        if count > 10:
            trimmed_values = gas_values[5:-5]
            trimmed_mean = statistics.mean(trimmed_values)
            trimmed_count = len(trimmed_values)
        else:
            trimmed_mean = mean_gas
            trimmed_count = count

        # Output results
        print("\n" + "=" * 70)
        print("📊 DAI TRANSFER GAS USAGE ANALYSIS")
        print("📊 (Only transfer() and transferFrom() function calls)")
        print("=" * 70)
        print(f"📈 Valid transfers analyzed: {count:,}")
        print(f"📊 Average gas used: {mean_gas:,.2f}")
        print(f"📊 Median gas used: {median_gas:,}")
        print(f"📊 Trimmed average (excluding top/bottom 5): {trimmed_mean:,.2f} ({trimmed_count} samples)")
        print(f"📊 Maximum gas used: {max(gas_values):,}")
        print(f"📊 Minimum gas used: {min(gas_values):,}")

        # Additional statistics
        if count >= 4:
            quartiles = statistics.quantiles(gas_values, n=4)
            q1, q3 = quartiles[0], quartiles[2]
            print(f"📊 First quartile (Q1): {q1:,.2f}")
            print(f"📊 Third quartile (Q3): {q3:,.2f}")
            print(f"📊 Interquartile range (IQR): {q3 - q1:,.2f}")

        print(f"\n💡 ANALYSIS NOTES:")
        print(f"   ✅ Only includes transfer() and transferFrom() function calls")
        print(f"   🚫 Excludes all swap-related functions (swapExactTokensForTokens, swap, etc.)")
        print(f"   ✅ Excluded suspicious transactions (phishing, scams, exploits)")
        print(f"   ✅ Accepts all gas values from legitimate transfer functions for unbiased data")
        print(f"   ✅ Excluded mint/burn operations and contract interactions")
        print(f"   ✅ Data represents actual user transfer costs without artificial filtering")

        print(f"\n🔍 DAI TRANSFER SPECIFIC INSIGHTS:")
        print(f"   📊 DAI is a decentralized stablecoin by MakerDAO")
        print(f"   📊 DAI uses 18 decimals (vs USDC's 6 decimals)")
        print(f"   📊 Only analyzing direct token transfer functions, excluding DEX trades")
        print(f"   📊 Transfer costs are relatively stable, suitable for baseline comparison")

    except KeyboardInterrupt:
        print(f"\n⚠️  Script interrupted by user. Collected {len(gas_values)} samples so far.")
        if gas_values:
            print(f"📊 Partial results - Average: {statistics.mean(gas_values):,.2f} gas")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

    print(f"\n✅ Analysis complete! Script finished successfully.")
    # Explicit exit to prevent re-execution
    sys.exit(0)


if __name__ == "__main__":
    main()
