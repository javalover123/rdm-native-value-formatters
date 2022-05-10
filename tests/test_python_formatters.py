import base64
from importlib import import_module
import io
import json
import sys
import unittest

import redis


REDIS_DB = 3

binary_values = [
    b'{"hello": "object"}',
    b'hello string'
]

expected_value = {'hello': 'dict'}


class TestBase(unittest.TestCase):
    expected_value = None

    def setUp(self):
        self.db = redis.Redis(db=3)

    def call_formatter(self):
        raise NotImplementedError()

    def get_formatted_output(self, base64_value):
        sys.stdin = io.StringIO(base64_value)
        stdout = sys.stdout
        sys.stdout = io.StringIO()

        self.call_formatter()

        sys.stdin = sys.__stdin__
        output = sys.stdout.getvalue()
        sys.stdout = stdout
        return output

    def check_formatting(self, value):
        base64_value = base64.b64encode(value).decode()
        json_output = self.get_formatted_output(base64_value)
        output = json.loads(json_output)
        formatted_value = output.get('output', '')

        if hasattr(self.expected_value, 'decode'):
            self.expected_value = self.expected_value.decode()

        self.assertEqual(formatted_value, self.expected_value,
                         'Unexpected output: {}'.format(formatted_value))


class TestPythonTimestampFormatter(TestBase):
    formatter = import_module('python-timestamp.formatter')
    value = "1651032779850"
    expected_value = "2022-04-27 12:12:59.850000"

    def call_formatter(self):
        self.formatter.TimestampFormatter().main('decode')

    def test_timestamp_formatter(self):
        key = 'format_demo_timestamp'
        self.db.set(key, self.value)
        self.check_formatting(self.db.get(key))


if __name__ == '__main__':
    unittest.main()
