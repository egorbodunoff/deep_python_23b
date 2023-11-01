from unittest import mock
from server import *
from client import *
import unittest


class TestServerClient(unittest.TestCase):
    def setUp(self) -> None:
        self.expected_urls = ["https://ru.wikipedia.org/wiki/Python",
                              "https://ru.wikipedia.org/wiki/Функция",
                              "https://ru.wikipedia.org/wiki/Роза"]

        self.urls = 'https://ru.wikipedia.org/wiki/Python\n' \
                    'https://ru.wikipedia.org/wiki/Функция\n' \
                    'https://ru.wikipedia.org/wiki/Роза'

        self.words = ["foo", "bar", "foo", "ee", "foo", "bar"]

    def test_create_urls(self):
        with mock.patch('builtins.open', mock.mock_open(read_data=self.urls)):
            result = create_urls('path/to/open')

        self.assertEqual(self.expected_urls, result)

        result_2 = create_urls("file_not_found")
        self.assertEqual([], result_2)

    def test_run_client_call(self):
        with mock.patch('builtins.open', mock.mock_open(read_data=self.urls)):
            with mock.patch("client.run_exp") as mock_exp:
                run_client('3', 'path/to/open')
                expected_calls = [
                    mock.call(self.expected_urls, 3),
                ]

            self.assertEqual(expected_calls, mock_exp.mock_calls)

        with self.assertRaises(ValueError) as err:
            run_client('not_number', 'dvd')
        self.assertEqual(ValueError, type(err.exception))

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






