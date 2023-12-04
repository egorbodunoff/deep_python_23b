from unittest import mock
from unittest.mock import patch
from fetcher import *
import unittest
import time


class TestFetcher(unittest.TestCase):
    @patch('builtins.open', mock.mock_open(read_data='q1\nq2\nq3\nq4\nq5'))
    def test_get_url(self):
        result = list(get_url('path/to/open'))

        self.assertEqual(result, ['q1', 'q2', 'q3', 'q4', 'q5'])

    def test_response_process(self):
        result = response_process('foo bar 1 2 foo 1 1', 2)

        self.assertEqual(result, {'1': 3, 'foo': 2})


class TestStuff(unittest.IsolatedAsyncioTestCase):
    @patch('fetcher.aiohttp.ClientSession.get')
    async def test_fetch_content(self, mock_session):
        response = mock.AsyncMock(status=200)

        async def text():
            return 'foo bar 1 3 joke joke joke foo'

        response.text = text
        mock_session.return_value.__aenter__.return_value = response

        result = await fetch_content('url')
        self.assertEqual(result, {'joke': 3, 'foo': 2})

    @patch('fetcher.aiohttp.ClientSession.get')
    async def test_fetch_content_bad_status(self, mock_session):
        response = mock.AsyncMock(status=100)
        response.text = lambda: 'foo bar 1 3 joke joke joke foo'

        mock_session.return_value.__aenter__.return_value = response

        result = await fetch_content('url')
        self.assertEqual(result, 'No connection')

    @patch('fetcher.aiohttp.ClientSession')
    async def test_fetch_connection_err(self, mock_session):
        mock_session.side_effect = aiohttp.ClientConnectionError

        result = await fetch_content('https://ru.wikipedia.org/wiki/Роза')

        self.assertEqual(result, 'Connection err')

    @patch('fetcher.aiohttp.ClientSession.get')
    async def test_fetch_invalid_url(self, mock_session):
        mock_session.side_effect = aiohttp.InvalidURL(1)

        result = await fetch_content('https://ru.wikipedia.org/wiki/Роза')

        self.assertEqual(result, 'Invalid URL')

    @patch('builtins.print')
    @patch('fetcher.aiohttp.ClientSession.get')
    async def test_num_batch_fetch(self, mock_session, mock_print):
        response = mock.AsyncMock(status=200)

        async def text():
            await asyncio.sleep(0.05)
            return 'foo bar 1 3 joke joke joke foo'

        response.text = text

        mock_session.return_value.__aenter__.return_value = response
        time_ls = []
        for i in range(1, 10, 2):
            start = time.time()
            await main('urls.txt', i)
            time_ls.append(time.time() - start)

            self.assertEqual(mock_print.call_args[0][0], {'foo': 2, 'joke': 3})

        for i in range(len(time_ls) - 1):
            self.assertGreater(time_ls[i], time_ls[i + 1])

    async def test_bad_arg(self):
        with self.assertRaises(ValueError) as err:
            await main('urls.txt', 'text')

        self.assertEqual(type(err.exception), ValueError)
