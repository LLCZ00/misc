"""
Omniserver

Command to generate self-signed TLS certificate & private key:
openssl req -new -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out cert.crt -keyout private.key
"""
import socket
import socketserver
import threading
import logging
import ssl
import sys
from time import sleep

"""
Constants
"""
BUFFERSIZE = 1024

"""
Helper functions
"""
def encode_data(data, encoding="utf-8"):
    if type(data) is not bytes:
        data = f"{data}\n".encode(encoding)
    return data


"""
Server Classes
"""
class TCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        client = f"{self.client_address[0]}:{self.client_address[1]}"
        logging.info(f"TCP connection from {client}")
        
        while True:
            data = self.request.recv(BUFFERSIZE).strip()
            if not data:
                break
            logging.info(f"Data recieved: {data.decode()}")
            response = "TCP server message"
            self.request.sendall(encode_data(response))
            logging.info(f"Response sent.")
        logging.info("Connection closed.\n")


class UDPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        client = f"{self.client_address[0]}:{self.client_address[1]}"
        data = self.request[0].strip()
        response = "UDP server message"        
        if data:
            logging.info(f"UDP data recieved from {client} - {data.decode()}")                                  
            self.request[1].sendto(encode_data(response), self.client_address)
            logging.info("UDP response sent.\n")


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True            
                
    def tls_setup(self, certfile: str, keyfile: str = None):
        """Method for enabling TLS/SSL on socket"""
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        self.socket = context.wrap_socket(self.socket, server_side=True)

        logging.debug("TLS enabled")
        
        
    def bind_and_activate(self):
        try:
            self.server_bind()
            self.server_activate()
            server_addr = self.socket.getsockname()
            logging.info(f"TCP server listening on {server_addr[0]}:{server_addr[1]}...\n")
        except:
            self.server_close()
            logging.error(f"Binding/activation failed")
            raise


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    allow_reuse_address = True
    daemon_threads = True
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        server_addr = self.socket.getsockname()
        logging.info(f"UDP server listening on {server_addr[0]}:{server_addr[1]}...\n")


"""
Client Classes
"""
class ClientBase:
    def __init__(self, ip: str, port: int, socket=None):
        self.ip = ip
        self.port = port
        self.sock = socket
        if self.sock is None:
            self.socket_setup()
            
    def socket_setup(self):
        """For differentiating between protocols"""
        raise NotImplementedError
        
    def recv(self): # Add option for custom buffersize     
        try:
            data = self.sock.recv(BUFFERSIZE).strip()
        except (socket.timeout, ConnectionRefusedError, ConnectionResetError):
            logging.error("Timeout/no response")
            return None
        else:
            logging.info(f"Data recieved: {data.decode()}")
            return data

    def close(self):
        if self.sock:
            self.sock.close()
    

class TCPClient(ClientBase):
    def socket_setup(self):
        """For differentiating between protocols"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def tls_setup(self):
        """Method for enabling TLS/SSL on socket"""
        context = ssl.create_default_context()
        self.sock = context.wrap_socket(self.sock, server_hostname=self.ip)
        logging.debug("TLS enabled")
        
    def connect(self) -> bool:
        """Attempt connection to ip:port, returns True upon success"""
        try:
            self.sock.connect((self.ip, self.port))
        except (socket.timeout, ConnectionRefusedError, ConnectionResetError):
            logging.error(f"Failed to establish TCP connection with {self.ip}:{self.port}")
            return False
        else:
            logging.info(f"Successfully established TCP connection with {self.ip}:{self.port}")
            return True
        
    def send(self, msg):
        self.sock.sendall(encode_data(msg))
        logging.info("Data sent.")
        
    def beacon(self, frequency: float = 5, tries: int = 0, timeout = None):
        self.sock.settimeout(timeout)
        attempt = 1
        while attempt != tries:
            if self.connect():
                return True
            attempt += 1
            sleep(frequency)
        return False    
         

class UDPClient(ClientBase):
    def socket_setup(self):
        """For differentiating between protocols"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def send(self, msg):
       self.sock.sendto(encode_data(msg), (self.ip, self.port))
       logging.info("UDP data sent.")
        
    def beacon(self, frequency: float = 5, tries: int = 0, timeout = None):
        self.sock.settimeout(timeout)
        attempt = 1
        while attempt != tries:
            self.send("Beacon message")
            if self.recv():
                return True
            attempt += 1
            sleep(frequency)
        return False
        

"""
Functions for interacting with core classes
"""      
def thread_wait(*servers):
    """Wait on threads"""
    try:
        while 1:
            sleep(1)
            sys.stderr.flush()
            sys.stdout.flush()
    except KeyboardInterrupt:
        pass
    finally:
        for server in servers:
            server.shutdown()
        logging.info("Omniserver closed.")

def tcp_server(ip: str, port: int, tls: bool = False):
    """Start TCP server, return server object"""
    server = ThreadedTCPServer((ip, port), TCPRequestHandler, bind_and_activate=False)
    if tls:
        server.tls_setup("./cert.crt", "./private.key")
    server.bind_and_activate()
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    return server

def udp_server(ip: str, port: int):
    server = ThreadedUDPServer((ip, port), UDPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    return server
 
def tcp_client(ip: str, port: int, tls: bool = False):
    client = TCPClient(ip, port)
    if tls:
        client.tls_setup()
    return client        

def udp_client(ip: str, port: int):
    return UDPClient(ip, port)

def main():
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")

    
    # server = tcp_server("0.0.0.0", 7896, tls=True)      
    # thread_wait(server)
    
    client = tcp_client("192.168.1.40", 7896)
    if client.connect():
        client.send("client test message")
        client.recv()

if __name__ == "__main__":
    main()

