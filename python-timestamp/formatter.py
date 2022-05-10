import os
import sys

import datetime
import re
import pytz

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from python_utils.base import BaseFormatter

__version__ = '0.0.1'
DESCRIPTION = 'Python timestamp to time native formatter'


class TimestampFormatter(BaseFormatter):
    description = DESCRIPTION
    version = __version__
    prog = re.compile(r"^\d{13}$")
    tz = pytz.timezone('Asia/Shanghai')

    def format(self, value):
        try:
            if self.prog.match(str(value, encoding="utf-8")):
                return datetime.datetime.fromtimestamp(int(value) / 1000, self.tz).strftime('%Y-%m-%d %H:%M:%S.%f')
        except ValueError as e:
            # return value
            return self.process_error('Cannot format value: {}'.format(e))
        return value


if __name__ == "__main__":
    TimestampFormatter().main()
