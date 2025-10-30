import zmq
import json
from const import *

class DBList:
    def __init__(self):
        self.value = []
    
    def append(self, data):
        self.value.append(data)
        return self.value
    
    def get_value(self):
        return self.value
    
    def search(self, data):
        try:
            return self.value.index(data)
        except ValueError:
            return -1
    
    def remove(self, data):
        try:
            self.value.remove(data)
            return True, self.value
        except ValueError:
            return False, self.value
    
    def insert(self, index, data):
        self.value.insert(index, data)
        return self.value
    
    def sort(self, reverse=False):
        self.value.sort(reverse=reverse)
        return self.value
    
    def clear(self):
        self.value = []
        return self.value
    
    def reverse(self):
        self.value.reverse()
        return self.value
    
    def pop(self, index=-1):
        try:
            return True, self.value.pop(index)
        except IndexError:
            return False, None

def server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:" + PORT)
    
    db_list = DBList()
    print(f"Servidor iniciado em tcp://*:{PORT}")
    
    while True:
        message = socket.recv()
        
        try:
            request = json.loads(message.decode())
            command = request.get("command")
            
            if command == "STOP":
                socket.send(json.dumps({"status": "ok"}).encode())
                break
            
            elif command == "append":
                result = db_list.append(request.get("data"))
                socket.send(json.dumps({"status": "ok", "result": result}).encode())
            
            elif command == "value":
                result = db_list.get_value()
                socket.send(json.dumps({"status": "ok", "result": result}).encode())
            
            elif command == "search":
                result = db_list.search(request.get("data"))
                socket.send(json.dumps({"status": "ok", "result": result}).encode())
            
            elif command == "remove":
                success, lista = db_list.remove(request.get("data"))
                socket.send(json.dumps({"status": "ok", "success": success, "result": lista}).encode())
            
            elif command == "insert":
                result = db_list.insert(request.get("index"), request.get("data"))
                socket.send(json.dumps({"status": "ok", "result": result}).encode())
            
            elif command == "sort":
                result = db_list.sort(request.get("reverse", False))
                socket.send(json.dumps({"status": "ok", "result": result}).encode())
            
            elif command == "clear":
                result = db_list.clear()
                socket.send(json.dumps({"status": "ok", "result": result}).encode())
            
            elif command == "reverse":
                result = db_list.reverse()
                socket.send(json.dumps({"status": "ok", "result": result}).encode())
            
            elif command == "pop":
                success, valor = db_list.pop(request.get("index", -1))
                socket.send(json.dumps({"status": "ok", "success": success, "result": valor}).encode())
            
            else:
                socket.send(json.dumps({"status": "error", "message": "Comando desconhecido"}).encode())
        
        except Exception as e:
            socket.send(json.dumps({"status": "error", "message": str(e)}).encode())
    
    print("Servidor encerrado")

if __name__ == "__main__":
    server()
