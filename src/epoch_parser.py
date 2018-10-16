from datetime import datetime
import math


class EpochParser(object):
    @staticmethod
    def parse(value: str) -> datetime:
        try:
            if value.isdigit():
                return EpochParser.__parse_timestamp(int(value))
            else:
                return None
        except ValueError:
            return None
        except OSError:
            return EpochParser.parse(str(math.ceil(int(value) / 1000)))

    @staticmethod
    def __parse_timestamp(timestamp: int) -> datetime:
        if timestamp > 86400:
            return datetime.fromtimestamp(timestamp)
        else:
            return datetime.fromtimestamp(86401)
