import zmq
import json
from const import *

def send_command(socket, command, **kwargs):
    request = {"command": command, **kwargs}
    socket.send(json.dumps(request).encode())
    response = socket.recv()
    return json.loads(response.decode())

def client():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{HOST}:{PORT}")
    
    print("=== Aplicação Cliente-Servidor com ZeroMQ ===\n")
    
    # Lista inicial
    resp = send_command(socket, "value")
    print("Lista inicial:", resp["result"])
    
    # Append
    send_command(socket, "append", data=5)
    send_command(socket, "append", data=6)
    send_command(socket, "append", data=3)
    send_command(socket, "append", data=8)
    resp = send_command(socket, "value")
    print("Após append(5, 6, 3, 8):", resp["result"])
    
    # Pesquisa
    resp = send_command(socket, "search", data=6)
    print("Busca por 6:", resp["result"])
    resp = send_command(socket, "search", data=10)
    print("Busca por 10:", resp["result"])
    
    # Insert
    send_command(socket, "insert", index=2, data=99)
    resp = send_command(socket, "value")
    print("Após insert(2, 99):", resp["result"])
    
    # Sort
    send_command(socket, "sort")
    resp = send_command(socket, "value")
    print("Após sort():", resp["result"])
    
    # Reverse
    send_command(socket, "reverse")
    resp = send_command(socket, "value")
    print("Após reverse():", resp["result"])
    
    # Remove
    resp = send_command(socket, "remove", data=99)
    print(f"Após remove(99): {resp['result']} - Sucesso: {resp['success']}")
    
    # Pop
    resp = send_command(socket, "pop")
    print(f"Após pop(): {resp['result']} - Lista:", end=" ")
    resp = send_command(socket, "value")
    print(resp["result"])
    
    # Clear
    send_command(socket, "clear")
    resp = send_command(socket, "value")
    print("Após clear():", resp["result"])
    
    # Finalizar servidor
    send_command(socket, "STOP")
    print("\nCliente encerrado")

if __name__ == "__main__":
    client()
