from bs4 import BeautifulSoup
from collections import Counter
import requests
import socket
import threading
import json
import argparse


def client_response(con, k):
    data = con.recv(1024)
    url = data.decode()

    words = url_process(url, con)
    if words is not None:
        popular_words = word_counter(words, k)
        json_data = json.dumps(popular_words, ensure_ascii=False)

        con.send(json_data.encode())
        con.close()


def url_process(url, con):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        words = soup.get_text().split()

        return words

    except requests.exceptions.ConnectionError:
        con.send(f" {url} не найдена".encode())
        con.close()

        return None


def word_counter(words, k):
    popular_words = dict()
    cnt = Counter(words)
    mc_words = cnt.most_common(k)

    for x in mc_words:
        popular_words[x[0]] = x[1]

    return popular_words


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 2023))
    server.listen()
    print("Server running")
    return server


def client_thread(server, k):
    try:
        while True:
            client, _ = server.accept()
            client_response(client, k)

    except KeyboardInterrupt:
        server.close()


def run_exp(n_threads, *arg):
    threads = [
        threading.Thread(
            target=client_thread,
            name=f"client-{i}",
            args=arg
        )
        for i in range(n_threads)
    ]

    for th in threads:
        th.start()

    for th in threads:
        th.join()


def run_server(w, k):
    if not w.isdecimal():
        raise ValueError("Количество потоков должно быть числом")

    if not k.isdecimal():
        raise ValueError("Количество слов, которых нужно вывести должно быть целым")

    working_server = start_server()
    run_exp(int(w), working_server, int(k))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', help='количество воркеров')
    parser.add_argument('-k', help='количество частых слов')

    args = parser.parse_args()
    W = args.w
    K = args.k
    run_server(W, K)
