### Client implementation ###

import socket
import argparse
from pathlib import Path


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
            "Port must be between 1 and 65535."
        )

    return value


def valid_file(value):
    file_path = Path(value)

    if not file_path.exists():
        raise argparse.ArgumentTypeError(
            f"File does not exist: {value}"
        )

    if not file_path.is_file():
        raise argparse.ArgumentTypeError(
            f"Path is not a file: {value}"
        )

    return file_path
    

def main():

    ## Parse and define input arguments
    parser = argparse.ArgumentParser(
        description="Send a file to a server."
    )
    # Define the server IP address
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Server IP address.",
    )
    # Define the server port
    parser.add_argument(
        "--port",
        type=valid_port,
        default=9000,
        help="Server TCP port.",
    )
    # Define the file and its path
    parser.add_argument(
        "--file_path",
        type=valid_file,
        required=True,
        help="Path to the file to transmit.",
    )

    args = parser.parse_args()


    ## Connect to server if possible
    try:
        with socket.socket() as client_socket:

            print("Connecting to server...")
            client_socket.connect((args.host, args.port))

            print("Connected!")

            ## Streaming file contents
            # Communication protocol
            filename_bytes = args.file_path.name.encode()
            client_socket.sendall(len(filename_bytes).to_bytes(4,"big"))    # send lenght of file name in 4 bytes
            client_socket.sendall(filename_bytes)                           # send file name
            file_size = args.file_path.stat().st_size
            client_socket.sendall(file_size.to_bytes(8,"big"))              # send file size in 8 bytes

            # Receive check from server whether to continue
            file_check = int.from_bytes(client_socket.recv(1),"big")

            # File does not exist in the designated directory on servers IP, continue
            if file_check == 0:
                print("Sending file...")

                # Stream file contents in chunks of size chunk_size
                sent_bytes = 0
                chunk_size = 4096

                with args.file_path.open("rb") as file:

                    while True:
                        chunk = file.read(chunk_size)

                        if not chunk:
                            break

                        client_socket.sendall(chunk)
                        sent_bytes += len(chunk)
                        progress = sent_bytes / file_size * 100

                        print(
                            f"\rUploading: {progress:.2f}% sent",
                            end=""
                        )

                    print(" - file sent successfully.")

                # Receive and print file transmition check from server
                recv_check = int.from_bytes(client_socket.recv(1),"big")

                if recv_check == 0:
                    print("File received successfully by the server.")
                else:
                    print("Unsuccessful file exchange.")

            # File exists, cancel tranfer
            elif file_check == 1:
                print("File already exists in the designated directory. Transfer cancelled by server.")

            else:
                print("Unexpected response from server.")

            print("Connection closed.")


    except ConnectionError as error:
        print(f"Connection error: {error}")



if __name__ == "__main__":
    main()