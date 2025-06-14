import urllib.request
import urllib.parse
import json
import statistics
import time

# ✅ Please fill in your Etherscan API Key
API_KEY = "YOUR_ETHERSCAN_API_KEY"
USDY_CONTRACT = "0x96F6eF951840721AdBF46Ac996b59E0235CB985C"
API_URL = "https://api.etherscan.io/api"


def make_request(params, retry_count=3):
    """Use the standard library to send HTTP requests,
    including retries and rate limiting"""
    url = f"{API_URL}?{urllib.parse.urlencode(params)}"

    for attempt in range(retry_count):
        try:
            # Add delay to avoid API rate limiting
            time.sleep(0.2)  # Each request interval is 200ms

            with urllib.request.urlopen(url, timeout=30) as response:
                result = json.loads(response.read().decode())

                # Check for API errors
                if result.get("message") == "NOTOK":
                    error_msg = result.get("result", "Unknown error")
                    if "rate limit" in error_msg.lower():
                        print(f"Trigger rate limit, wait 2 seconds and try again... (try {attempt + 1}/{retry_count})")
                        time.sleep(2)
                        continue
                    else:
                        print(f"API Error: {error_msg}")
                        return None

                return result

        except Exception as e:
            print(f"Request failed (try {attempt + 1}/{retry_count}): {e}")
            if attempt < retry_count - 1:
                time.sleep(1)  # Wait 1 second to try again after failure

    return None


def fetch_transfers(page=1, offset=100):
    """Get USDY transfer transaction hash - only contains real transfers"""
    params = {
        "module": "account",
        "action": "tokentx",
        "contractaddress": USDY_CONTRACT,
        "page": page,
        "offset": offset,
        "sort": "desc",
        "apikey": API_KEY
    }

    resp = make_request(params)
    if not resp or resp.get("status") != "1":
        print(f"Failed to obtain transaction: {resp}")
        return []

    transfer_hashes = []
    for tx in resp["result"]:
        # Filter by:
        # 1. from is not the 0 address (excluding mint)
        # 2. to is not 0 address (excluding burn)
        # 3. Neither from nor to is the contract address itself (excluding some special operations)
        if (tx["from"] != "0x0000000000000000000000000000000000000000" and
                tx["to"] != "0x0000000000000000000000000000000000000000" and
                tx["from"].lower() != USDY_CONTRACT.lower() and
                tx["to"].lower() != USDY_CONTRACT.lower()):
            transfer_hashes.append(tx["hash"])

    return transfer_hashes


def fetch_gas_used(tx_hash):
    """Get the gas usage of a single transaction and verify whether it is a transfer function call"""
    # Get transaction details first
    tx_params = {
        "module": "proxy",
        "action": "eth_getTransactionByHash",
        "txhash": tx_hash,
        "apikey": API_KEY
    }

    tx_resp = make_request(tx_params)
    if tx_resp and tx_resp.get("result"):
        tx_data = tx_resp["result"]
        input_data = tx_data.get("input", "")

        # Check whether it is a transfer function call
        # The function signature of transfer(address,uint256) is 0xa9059cbb
        # transferFrom(address,address,uint256) function signature is 0x23b872dd
        if not (input_data.startswith("0xa9059cbb") or input_data.startswith("0x23b872dd")):
            return None  # Not a transfer related function, skip

    # Get the gas usage in the transaction receipt
    receipt_params = {
        "module": "proxy",
        "action": "eth_getTransactionReceipt",
        "txhash": tx_hash,
        "apikey": API_KEY
    }

    receipt_resp = make_request(receipt_params)
    if not receipt_resp:
        return None

    result = receipt_resp.get("result")
    if result and result.get("gasUsed"):
        return int(result["gasUsed"], 16)
    return None


def main():
    target_transfer_count = 200
    print(f"Start getting {target_transfer_count}th USDY Transfer transaction data...")
    print("⚠️  To avoid API rate limits, each request is delayed by 200ms. Please be patient...")

    gas_values = []
    page = 1
    total_processed = 0

    while len(gas_values) < target_transfer_count:
        print(f"\nGetting Page {page} transaction data...")
        tx_hashes = fetch_transfers(page=page, offset=100)

        if not tx_hashes:
            print("No more transaction data available")
            break

        transfer_found_in_page = 0

        for tx in tx_hashes:
            total_processed += 1
            gas = fetch_gas_used(tx)

            if gas is not None:  # Is a valid transfer transaction
                gas_values.append(gas)
                transfer_found_in_page += 1
                print(f"[{len(gas_values)}/{target_transfer_count}] {tx} → gasUsed: {gas:,}")

                if len(gas_values) >= target_transfer_count:
                    break

            # The progress is displayed every 10 transactions.
            if total_processed % 10 == 0:
                print(f"Processed {total_processed} Transactions, found {len(gas_values)} valid transfer...")

        print(f"Page {page} found {transfer_found_in_page} valid transfer txn")
        page += 1

        # If you don't find a transfer transaction for several consecutive pages, you may need to stop
        if transfer_found_in_page == 0:
            print("No valid transfer transaction found on the current page, continue to try the next page...")

    if not gas_values:
        print("Failed to get any valid transfer gas data.")
        return

    print(f"\n✅ Successfully collected {len(gas_values)} transaction, totally handled {total_processed} transaction")

    # Statistical analysis
    gas_values.sort()
    count = len(gas_values)
    median_gas = statistics.median(gas_values)
    mean_gas = statistics.mean(gas_values)

    # Calculate the trimmed average (remove the highest and lowest 5)
    if count > 10:
        trimmed_values = gas_values[5:-5]
        trimmed_mean = statistics.mean(trimmed_values)
    else:
        trimmed_mean = mean_gas

    # Output statistical results
    print("\n" + "=" * 60)
    print("📊 USDY Transfer Gas usage statistics (transfer, transferFrom only): ")
    print("=" * 60)
    print(f"• Number of valid transfers: {count}")
    print(f"• Average gasUsed: {mean_gas:,.2f}")
    print(f"• Median: {median_gas:,}")
    print(f"• Trimmed average (remove the highest/lowest 5 strokes): {trimmed_mean:,.2f}")
    print(f"• Maximum value: {max(gas_values):,}")
    print(f"• Minimum: {min(gas_values):,}")

    # Additional statistics
    q1 = statistics.quantiles(gas_values, n=4)[0]
    q3 = statistics.quantiles(gas_values, n=4)[2]
    print(f"• Quartile 1 (Q1): {q1:,.2f}")
    print(f"• Third Quartile (Q3): {q3:,.2f}")
    print(f"• Interquartile Range (IQR): {q3 - q1:,.2f}")

    print(f"\n💡 Analysis Notes: ")
    print(f"   - Only transfer(address,uint256) and transferFrom(address,address,uint256) functions are counted.")
    print(f"   - Excluded high gas consumption operations such as mint, burn, send, etc.")
    print(f"   - The data accurately reflects the gas cost of ordinary users' transfers.")


if __name__ == "__main__":
    main()
