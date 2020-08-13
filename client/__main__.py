from config import HEADERSIZE, IP, PORT
import json
import socket

class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.sock.connect((IP, PORT))
        self.send(type='job_req')
        self.handle_connection()

    def handle_connection(self):
        new_data = True
        new = b""

        while True:
            data = self.sock.recv(1024)

            if data == b"":
                continue

            if new_data:
                new_data = False
                full_data = b""

                data = new + data

                new = b""
                data_len = int(data[:HEADERSIZE].decode("utf-8"))
                full_data += data[HEADERSIZE:]
            else:
                full_data += data

            if len(full_data) >= data_len:
                new_data = True

                new = full_data[data_len:]
                full_data = full_data[:data_len]

                self.handle_data(full_data)
                full_data = b""

    def handle_data(self, data):
        data = json.loads(data.decode('utf-8'))

        if data['type'] == 'error':
            print(data['error'])
        if data['type'] == 'job':
            print(f"New job recieved from server. range: {data['range']}")
            result = self.start_calculation(data['range'])
            self.send(type='result', result=result)

    def send(self, **kwargs):
        data = json.dumps(kwargs).encode('utf-8')

        self.sock.send(str(len(data)).ljust(HEADERSIZE).encode('utf-8') + data)

    def start_calculation(self, _range):
        result = []

        for num in range(_range[0], _range[1]):
            is_prime = True
            for j in range(2, num):
                if num % j == 0:
                    is_prime = False
                    break
            if is_prime:
                print(f"Found prime: {num}")
                result.append(num)

        return result

def main():
    global client
    client = Client()
    client.start()

if __name__ == "__main__":
    main()
