import requests
import datetime
import time

def get_block_height_at_time(timestamp):
    url = f"https://blockchain.info/blocks/{timestamp}?format=json"
    response = requests.get(url)
    if response.status_code == 200:
        blocks = response.json()
        if blocks:
            return blocks[0]['height']
    return None

def get_block_hash(height):
    url = f"https://blockchain.info/block-height/{height}?format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['blocks'][0]['hash']
    return None

def get_transactions_for_block(block_hash):
    url = f"https://blockchain.info/rawblock/{block_hash}"
    response = requests.get(url)
    if response.status_code == 200:
        block_data = response.json()
        return block_data.get('tx', [])
    return []

def get_transactions_in_time_range(start_time, end_time):
    start_height = get_block_height_at_time(int(start_time.timestamp() * 1000))
    end_height = get_block_height_at_time(int(end_time.timestamp() * 1000))
    
    if start_height is None or end_height is None:
        return []

    all_transactions = []
    for height in range(start_height, end_height + 1):
        block_hash = get_block_hash(height)
        if block_hash:
            transactions = get_transactions_for_block(block_hash)
            all_transactions.extend(transactions)
            print(f"Processed block at height {height}")
            time.sleep(1)  # Để tránh vượt quá giới hạn rate
    return all_transactions

# Sử dụng
start_date = datetime.datetime(2024, 6, 21)
end_date = datetime.datetime(2024, 6, 21, 0, 0, 2)  # 1 giờ sau

transactions = get_transactions_in_time_range(start_date, end_date)
print(f"Số lượng giao dịch: {len(transactions)}")
for tx in transactions[:5]:  # In 5 giao dịch đầu tiên
    print(f"Transaction hash: {tx}")