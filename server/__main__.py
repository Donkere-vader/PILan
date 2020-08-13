from config import HEADERSIZE, IP, PORT, JOB_SIZE
from console import Console
import threading
import socket
import json


class Server:
    def __init__(self):
        self.console = Console()
        self.connections = []
        self.threads = []
        self.numbers = []

        self.output_file = open('numbers.txt', 'a')

        _min = int(self.console.input("Minimum value: "))

        try:
            _max = int(self.console.input("Maximum value (leave blank if None): "))
        except ValueError:
            _max = 0

        self.range = (_min, _max)

        self.calculated_range = [0, 0]

        self.start()

    def start(self):
        self.console.log("Starting server...")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((IP, PORT))
        self.sock.listen(5)

        self.console.log(f"Server online @ ({socket.gethostbyname(socket.gethostname())}, {PORT})")

        # listen for connection attempts

        while True:
            connection, address = self.sock.accept()
            self.connections.append(connection)
            self.console.log(f"New connection with {address}")

            # start a thread for this user
            new_thread = threading.Thread(target=self.handle_connection, args=(connection, address))
            self.threads.append(new_thread)
            new_thread.daemon = True
            new_thread.start()

    def handle_connection(self, connection, address):
        new_data = True
        new = b""

        while True:
            try:
                data = connection.recv(1024)
            except (ConnectionResetError, ConnectionAbortedError):
                self.console.log(f"Lost connection with {address}", negative=True)
                self.connections.remove(connection)
                return

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

                self.handle_data(full_data, connection)
                full_data = b""

    def handle_data(self, data, connection):
        data = json.loads(data.decode('utf-8'))

        if data['type'] == 'error':
            self.console.log(data['error'], negative=True)

        if data['type'] == 'job_req':
            self.give_job(connection)

        if data['type'] == 'result':
            self.numbers += data['result']
            self.console.log(f"New numbers: [{data['result'][0]} ... {data['result'][-1]}]")
            self.save_result(data['result'])
            self.give_job(connection)

    def give_job(self, connection):
        job_range = self.get_job_range()
        if job_range is None:
            self.console.log("All jobs finished")
            return
        self.send(connection, type='job', range=job_range)

    def get_job_range(self):
        if self.calculated_range[1] + JOB_SIZE > self.range[1] and self.range[1] != 0:
            _max = self.range[1]
        else:
            _max = self.calculated_range[1] + JOB_SIZE

        _min = self.calculated_range[1] + 1
        if _min > self.range[1] and self.range[1] != 0:
            return None

        self.calculated_range[1] = _max
        return [_min, _max]

    def save_result(self, result):
        for num in result:
            self.output_file.write(str(num) + '\n')

    def send(self, connection, **kwargs):
        data = json.dumps(kwargs).encode('utf-8')
        connection.send(str(len(data)).ljust(HEADERSIZE).encode('utf-8') + data)

def main():
    global server
    server = Server()

if __name__ == "__main__":
    main()
