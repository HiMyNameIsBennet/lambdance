# implement connection listener on localhost port 8888 in order to retrieve user secret from oauth callback
import socket


def launch_callback_server():
    server = socket.socket()
    host = "127.0.0.1"
    port = 8888

    server.bind((host, port))

    server.listen()

    # put this in a side thread?
    # see https://stackoverflow.com/questions/21153262/sending-html-through-python-socket-server
    client, _ = server.accept()
    
    rec = client.recv(4096).decode("ascii").split("\r\n")

    # find a way to extract this stuff cleaner
    return_creds_string = rec[0].split("?")[1]
    return_creds = return_creds_string.split("&")

    # handle unsuccessful response, see api tutorial
    user_code = return_creds[0][5:]
    return_state = return_creds[1][6:22]


    client.send(b"HTTP/1.0 200 OK\n")
    client.send(b"Content-Type: text/html\n")
    client.send(b'\n')

    client.send(b"""
        <html>
        <body>
        <h1>Connection Successful!</h1>
        </body>
        </html>
    """)
    client.close()
    
    server.close()

    return (user_code, return_state)
