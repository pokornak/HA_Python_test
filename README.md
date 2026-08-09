# Client - Server App

This project implements a simple client-server application for transferring files over a TCP connection using Python.

The server listens for incoming client connections and saves transmitted files to a designated directory. The client connects to the server, sends a selected file in chunks, and displays the transfer progress. The application currently handles one file transfer per connection. Already existing files are not overwritten.

The application is designed as a simple command-line tool and uses only Python's standard library. It has been developed and tested in Python 3.13.

---

## Project structure
### `server.py`
Validates the input directory and creates it if necessary. Starts the TCP server, accepts client connection, receives file metadata and if the file does not already exist, it receives and saves the file in chunks to the designated directory while displaying the progress. If the file already exists it cancels the transfer. It informs the client about the file prior existence and subsequently the reception completion.

### `client.py`
Validates the input file, connects to the server, streams file metadata and contents, and displays transmission progress.

### `README.md`
Contains project documentation, setup instructions, usage information, and a description of the communication protocol.

---

## Configuration and usage
Both `server.py` and `client.py` accept configuration through command-line arguments. Run either program with `--help` to see the available arguments.

#### 1. Start `server.py`
   
| Argument | Description | Required | Default value | Example |
| :--- | :--- | :---: | :---: | :---: |
| `--host` | Address on which the server listens | NO | `"127.0.0.1"` | `"0.0.0.0"`|
| `--port` | TCP port used by the server  | NO | `9000` | `5000` |
| `--directory` | Directory where received files are saved | NO | `./received` | `./newdir/subdir` |

Example: `python3 server.py --host 0.0.0.0 --port 5000 --directory ./newdirectory`

#### 2. Start `client.py`
   
| Argument | Description | Required | Default value | Example |
| :--- | :--- | :---: | :---: | :---: |
| `--host` | IP address or hostname of the server | NO | `"127.0.0.1"` | `"192.168.1.10"`|
| `--port` | TCP port used by the server  | NO | `9000` | `4000` |
| `--file_path` | Path to the file to be transmitted | YES | - | `./dir/example.pdf` |

Example: `python3 client.py --host 127.0.0.1 --port 5000 --file_path ./example.txt`

#### 3a. Example `server.py` output  
    Waiting for connection...  
    Client connected from ('127.0.0.1', 55798)  
    Receiving data...  
    100.00% received - file received successfully.  
    Connection closed.

#### 3b. Example `client.py` output  
    Connecting to server...
    Connected!
    Sending file...
    Uploading: 100.00% sent - file sent successfully.
    File received successfully by the server.
    Connection closed.

---

## Communication protocol
![](https://github.com/pokornak/HA_Python_test/blob/main/comm_protocol.png)

## Error handling and testing
The application validates the command-line input before attempting the file transfer. It was briefly tested for the following scenarios.

File transfer:
- Client and server running on the same machine.
- Successful transfer of smaller and larger pdf, jpeg, pptx and other files.
- File already exists in the designated directory.
- The designated directory does not exist.

Invalid input:  
- Input file does not exist.
- Input path is a directory rather than a file.
- Invalid port number.
- Invalid destination directory path.

Connection error:
- Server cannot be reached.
- Connection is unexpectedly closed during transmission.

