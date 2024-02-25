import tkinter as tk
import socket

class BluetoothClient:
    def __init__(self, host, port, gui):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.gui = gui # Set to None or make a setter function. Maybe take out having to set the GUI in the runner

    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print("Connected to server.")
            self.receive_data()
        except Exception as e:
            print(f"Connection error: {e}")

    def send_data(self, data):
        try:
            self.client_socket.send(data.encode('utf-8'))
        except Exception as e:
            print(f"Error sending data: {e}")

    def receive_data(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                self.gui.update_received_data(data.decode('utf-8'))
            except Exception as e:
                print(f"Error receiving data: {e}")
                break

class BluetoothGUI:
    def __init__(self, master, client):
        self.master = master
        master.title("Bluetooth Tkinter GUI")

        self.client = client

        self.label = tk.Label(master, text="Enter text to send:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.send_button = tk.Button(master, text="Send via Bluetooth", command=self.send_data)
        self.send_button.pack()

        self.received_data_label = tk.Label(master, text="Received data will appear here:")
        self.received_data_label.pack()

        # Connect to the server
        self.client.connect()

    def send_data(self):
        data_to_send = self.entry.get()
        self.client.send_data(data_to_send)

    def update_received_data(self, data):
        self.received_data_label.config(text=f"Received data: {data}")

if __name__ == "__main__":
    # Replace '00:00:00:00:00:00' with the Bluetooth address of the server device
    server_bluetooth_address = '5c:fb:3a:53:e8:3e'
    server_port = 4

    server = BluetoothClient(server_bluetooth_address, server_port, None)  # Pass None for now

    root = tk.Tk()
    app = BluetoothGUI(root, server)
    server.gui = app  # Assign the GUI instance to the client
    root.mainloop()