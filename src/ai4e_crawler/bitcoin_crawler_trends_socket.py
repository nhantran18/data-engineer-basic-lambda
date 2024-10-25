import websocket
import json
import ssl

def on_message(ws, message):
    data = json.loads(message)
    print(f"Received new transaction: {data}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### Connection closed ###")

def on_open(ws):
    print("Connection established")
    # Đăng ký nhận thông tin về giao dịch chưa được xác nhận
    ws.send(json.dumps({"op": "unconfirmed_sub"}))

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.blockchain.info/inv",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})