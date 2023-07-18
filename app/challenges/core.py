from llama_cpp import Llama
from sys import argv
from app import app
import socket
import threading


def load_llm():
    log = open("/challenge/log.txt", "w")
    log.write("")
    log.close()
    print("Loading LLM...")
    llm = Llama(model_path="/challenge/models/ggml-old-vic13b-q4_0.bin", n_ctx=2048)
    log = open("/challenge/log.txt", "a")
    log.write("LLM loaded!")
    log.close()
    return llm


def start_server(llm:Llama, port:int):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(1)
    while True:
        i = 0
        conn, addr = server.accept()
        print('Connected by', addr)
        proc = threading.Thread(target=app, args=(conn, i, llm))
        proc.start()
    server.close()


port = int(argv[1])
llm = load_llm()
start_server(llm, port)
