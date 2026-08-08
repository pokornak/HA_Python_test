### Server implementation ###

import socket
import argparse
from pathlib import Path


## Function ensuring complete receiving
def recv_exact(sock, amount):
    """ 
        sock: socket.socket
            connected client socket
        amount: int
            amount of bytes expected to receive
    """

    data = b""

    while len(data) < amount:
        chunk = sock.recv(amount - len(data))

        if not chunk:
            raise ConnectionError(
                "Connection closed"
            )

        data += chunk

    return data

## Function for receiving file content in chunks if the file does not already exist
def receive_file(client_socket, destination, file_size):
    """ 
        client_socket: socket.socket
                    connected client socket
        destination: pathlib.Path
                    designated directory and file name
        file_size: int
                    file size in bytes
    """

    # File does already exist in the directory, inform client
    if destination.exists():
        print("File already exists. Transfer cancelled.")
        client_socket.sendall((1).to_bytes(1,"big"))
        return

    # Continue with file receivement, inform client
    else:
        client_socket.sendall((0).to_bytes(1,"big"))
        print("Receiving data...")

        # Receive file contents in chunks of max size 4096
        remaining = file_size

        with destination.open("wb") as file:

            while remaining > 0:

                chunk_size = min(4096, remaining)
                chunk = client_socket.recv(chunk_size)

                if not chunk:
                    raise ConnectionError(
                        "Client disconnected during transfer."
                    )

                file.write(chunk)

                remaining -= len(chunk)
                progress = (file_size - remaining) / file_size * 100
                print(
                    f"\r{progress:.2f}% received",
                    end=""
                )

        print(" - file received successfully.")
        client_socket.sendall((0).to_bytes(1,"big"))
        return


## Functions validating input arguments
def valid_port(value):
    try:
        value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Port must be an integer."
        )

    if not 1 <= value <= 65535:
        raise argparse.ArgumentTypeError(
            "Invalid port number: port must be between 1 and 65535."
        )

    return value


def valid_directory(value):
    path = Path(value)

    if path.exists() and not path.is_dir():
        raise argparse.ArgumentTypeError(
            f"Invalid directory: path exists but is not a directory: {value}"
        )

    return path



def main():

    ## Parse and define input arguments
    parser = argparse.ArgumentParser(
        description="File transfer server."
    )
    # Define the host IP address
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="IP address on which the server listens.",
    )
    # Define the port
    parser.add_argument(
        "--port",
        type=valid_port,
        default=9000,
        help="TCP port on which the server listens.",
    )
    # Define the designated directory
    parser.add_argument(
        "--directory",
        type=valid_directory,
        default=Path("./received"),
        help="Directory where received files are saved.",
    )

    args = parser.parse_args()


    ## Create the nonexistent directory
    try:
        args.directory.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        print(f"Invalid directory name: {error}")


    ## Create the network
    with socket.socket() as server_socket:

        server_socket.bind((args.host, args.port))

        print("Waiting for connection...")
        server_socket.listen()

        # Accept client if possible
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Client connected from {client_address}")

            with client_socket:

                ## Receive file name and file contents
                filename_size = int.from_bytes(recv_exact(client_socket,4),"big")
                filename = recv_exact(client_socket,filename_size).decode()
                file_size = int.from_bytes(recv_exact(client_socket,8),"big")

                receive_file(client_socket,args.directory / filename,file_size)

                print("Connection closed.")

        except ConnectionError as error:
            print(f"Connection error: {error}")



if __name__ == "__main__":
    main()