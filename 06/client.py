from queue import Queue
import socket
import threading
import argparse


def run_exp(urls, m):
    que = Queue(maxsize=100)
    threads = [
        threading.Thread(
            target=create_client,
            name=f"fetch-{i}",
            args=(que,)
        )
        for i in range(m)
    ]

    for th in threads:
        th.start()

    for url in urls:
        que.put(url)
    que.put(None)

    for th in threads:
        th.join()


def create_client(que):
    while True:
        url = que.get()

        if url is None:
            que.put(url)
            break

        client = socket.socket()
        client.connect(("localhost", 2023))

        client.send(url.encode())
        data = client.recv(1024)
        print("Server sent: ", data.decode(encoding="utf-8"), "\n")
        client.close()


def create_urls(file_name):
    urls = []

    try:
        with open(file_name, "r") as file:
            for row in file:
                urls.append(row.rstrip())
    except FileNotFoundError:
        print("Файл с таким именем не был найден")

    return urls


def run_client(m, file_name):
    if not m.isdecimal():
        raise ValueError("Количество потоков должно быть числом")

    urls = create_urls(file_name)
    run_exp(urls, int(m))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-M', help="количество потоков")
    parser.add_argument('-f', help="файл с URL'ами")

    args = parser.parse_args()
    M = args.M
    f = args.f

    run_client(M, f)
