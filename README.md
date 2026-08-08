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


## Configuration
Both `server.py` and `client.py` accept configuration through command-line arguments. Run either program with `--help` to see the available arguments.
### `server.py`
| Argument | Description | Required | Default value | Example |
| :--- | :--- | :---: | :---: | :---: |
| `--host` | Address on which the server listens | NO | `"127.0.0.1"` | `"0.0.0.0"`|
| `--port` | TCP port used by the server  | NO | `9000` | `5000` |
| `--directory` | Directory where received files are saved | NO | `./received` | `./newdir/subdir` |

### `client.py`
| Argument | Description | Required | Default value | Example |
| :--- | :--- | :---: | :---: | :---: |
| `--host` | IP address or hostname of the server | NO | `"127.0.0.1"` | `"192.168.1.10"`|
| `--port` | TCP port used by the server  | NO | `9000` | `4000` |
| `--file_path` | Path to the file to be transmitted | YES | - | `./dir/example.pdf` |



