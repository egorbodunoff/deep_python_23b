from unittest import mock
from unittest.mock import patch
from server import *
from client import *
import unittest
import time


class TestServerClient(unittest.TestCase):
    def setUp(self) -> None:
        self.text = ('В основе ежедневной работы пользователей в сети'
                     ' Интернет лежит обмен данными между клиентскими'
                     ' приложениями (например браузер) и веб-серверами.'
                     ' В соответствии с прикладным протоколом HTTP,'
                     ' клиент отправляет запрос (request) на получение'
                     ' определенного ресурса к серверу и получает от него'
                     ' ответ (response). Ответ, помимо самого запрошенного ресурса,'
                     ' содержит также служебную информацию.')

        self.expected_urls = ["https://ru.wikipedia.org/wiki/Python",
                              "https://ru.wikipedia.org/wiki/Функция",
                              "https://ru.wikipedia.org/wiki/Роза"]

        self.urls = 'https://ru.wikipedia.org/wiki/Python\n' \
                    'https://ru.wikipedia.org/wiki/Функция\n' \
                    'https://ru.wikipedia.org/wiki/Роза'

        self.words = ["foo", "bar", "foo", "ee", "foo", "bar"]

    def test_create_urls(self):
        with patch('builtins.open', mock.mock_open(read_data=self.urls)):
            result = list(create_urls('path/to/open'))

        self.assertEqual(self.expected_urls, result)

        result_2 = list(create_urls("file_not_found"))
        self.assertEqual([None], result_2)

    def test_run_client_call(self):
        with self.assertRaises(ValueError) as err:
            run_client('not_number', 'dvd')
        self.assertEqual(ValueError, type(err.exception))

    @patch('builtins.print')
    @patch('client.Queue')
    def test_create_client(self, mock_queue, mock_print):
        mock_queue.get.side_effect = ['https://ru.wikipedia.org/wiki/Python', None]
        with mock.patch('socket.socket') as mock_socket:
            mock_socket.return_value.recv.return_value = 'response received'.encode()
            create_client(mock_queue)

            self.assertEqual('Server sent: response received\n',
                             ''.join(mock_print.call_args[0]))

    @patch('builtins.print')
    @patch('server.requests')
    def test_response(self, mock_requests, mock_print):
        mock_response = mock.MagicMock()
        mock_response.text = self.text

        mock_requests.get.return_value = mock_response

        th = threading.Thread(target=run_server, args=('3', '2'))
        th.start()

        run_client('2', 'urls.txt')

        self.assertEqual('Server sent: {"В": 2, "и": 2}\n',
                         ''.join(mock_print.call_args[0]))

        time.sleep(5)

    @patch('builtins.print')
    @patch('server.requests')
    def test_time_dependence_on_workers(self, mock_requests, mock_print):
        mock_response = mock.MagicMock()
        mock_response.text = self.text
        mock_requests.get.return_value = mock_response

        th = threading.Thread(target=run_server, args=('1', '2'))
        th.start()
        start = time.time()
        for i in range(5):
            run_client('1', 'urls.txt')
        time1 = time.time() - start

        time.sleep(5)

        th = threading.Thread(target=run_server, args=('3', '2'))
        th.start()
        start1 = time.time()
        for i in range(5):
            run_client('3', 'urls.txt')
        time2 = time.time() - start1

        time.sleep(5)

        th = threading.Thread(target=run_server, args=('8', '2'))
        th.start()
        start = time.time()
        for i in range(5):
            run_client('8', 'urls.txt')
        time3 = time.time() - start

        self.assertGreater(time1, time2)
        self.assertGreater(time2, time3)
        self.assertGreater(time1, time3 * 5)

    def test_word_counter(self):
        res = word_counter(self.words, 2)
        self.assertEqual({"foo": 3, "bar": 2}, res)

        res = word_counter(self.words, 3)
        self.assertEqual({"foo": 3, "bar": 2, "ee": 1}, res)

    def test_run_server(self):
        with mock.patch("server.start_server") as mock_serv:
            with mock.patch('socket.socket') as mock_socket:
                mock_serv.return_value = mock_socket
            with mock.patch("server.run_exp") as mock_exp:
                run_server('3', '3')
                expected_calls = [
                    mock.call(3, mock_socket, 3),
                ]

            self.assertEqual(expected_calls, mock_exp.mock_calls)

    def test_run_client(self):
        with mock.patch('builtins.print') as mock_print:
            with mock.patch('socket.socket') as mock_socket:
                mock_socket.return_value.recv.return_value = "server run".encode()
                with mock.patch('builtins.open', mock.mock_open(read_data=self.urls)):
                    run_client('3', 'path/to/open')

        for resp in mock_print.call_args_list:
            self.assertEqual("server run", resp[0][1])
