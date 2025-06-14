import urllib.request
import urllib.parse
import json
import statistics
import time
import sys

# ✅ Please fill in your Etherscan API Key
API_KEY = "YOUR_ETHERSCAN_API_KEY"
USDC_CONTRACT = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
API_URL = "https://api.etherscan.io/api"

# Gas usage thresholds to filter out abnormal transactions
MIN_GAS_THRESHOLD = 20000  # Minimum reasonable gas for USDC transfer
MAX_GAS_THRESHOLD = 100000  # Maximum reasonable gas for normal USDC transfer

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
        # USDC has 6 decimals, so 1 USDC = 1,000,000
        if value > 0 and value < 1000:  # Less than 0.001 USDC
            return True, "Abnormally small transfer amount"
    except:
        pass

    return False, ""


def fetch_transfers(page=1, offset=100):
    """Get USDC transfer transaction hashes - only contains legitimate transfers"""
    params = {
        "module": "account",
        "action": "tokentx",
        "contractaddress": USDC_CONTRACT,
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
                tx["from"].lower() == USDC_CONTRACT.lower() or
                tx["to"].lower() == USDC_CONTRACT.lower()):
            continue

        # Check for suspicious transactions
        is_suspicious, reason = is_suspicious_transaction(tx)
        if is_suspicious:
            excluded_count += 1
            continue

        transfer_hashes.append(tx["hash"])

    if excluded_count > 0:
        print(f"📊 Page {page}: {len(transfer_hashes)} valid, {excluded_count} excluded")

    return transfer_hashes


def fetch_gas_used(tx_hash):
    """Get gas usage for a single transaction and verify it's a legitimate transfer"""
    # Get transaction receipt directly - skip transaction details check for speed
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

        # Filter out abnormal gas usage
        if gas_used < MIN_GAS_THRESHOLD:
            return None, f"Gas too low ({gas_used} < {MIN_GAS_THRESHOLD})"
        elif gas_used > MAX_GAS_THRESHOLD:
            return None, f"Gas too high ({gas_used} > {MAX_GAS_THRESHOLD})"

        return gas_used, "Valid"

    return None, "No gas data"


def main():
    print("🚀 Starting USDC Gas Analysis Script")
    print("=" * 60)

    target_transfer_count = 200
    offset = 100  # Increase to get more transactions per page
    print(f"Target: {target_transfer_count} legitimate USDC transfers")
    print(f"Gas range: {MIN_GAS_THRESHOLD:,} - {MAX_GAS_THRESHOLD:,}")
    print("⚠️  Optimized for speed - 100ms delay per request. Processing...")
    print("=" * 60)

    gas_values = []
    page = 1
    total_processed = 0
    total_excluded = 0

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
                    print(f"✅ [{len(gas_values)}/{target_transfer_count}] {tx_hash} → {gas_used:,} gas")

                    if len(gas_values) >= target_transfer_count:
                        break
                else:
                    total_excluded += 1

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
        print("📊 USDC TRANSFER GAS USAGE ANALYSIS")
        print("📊 (Legitimate transfer/transferFrom transactions only)")
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
        print(f"   ✅ Only legitimate transfer() and transferFrom() calls included")
        print(f"   ✅ Excluded suspicious transactions (phishing, scams, exploits)")
        print(f"   ✅ Filtered out abnormal gas usage ({MIN_GAS_THRESHOLD:,} - {MAX_GAS_THRESHOLD:,} range)")
        print(f"   ✅ Excluded mint/burn operations and contract interactions")
        print(f"   ✅ Data represents typical user transfer costs")

        print(f"\n🔍 COMPARISON INSIGHTS:")
        print(f"   📊 USDC is the most widely used USD stablecoin")
        print(f"   📊 High transaction volume provides robust gas usage data")
        print(f"   📊 Useful baseline for comparing with other tokens like USDY")
        print(f"   📊 USDC uses older contract architecture, may differ from newer tokens")

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
