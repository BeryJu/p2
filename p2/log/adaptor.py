from collections import ChainMap
from enum import Enum
from time import time
from uuid import uuid4


class RecordType(Enum):

    DEBUG = 0
    INFO = 1
    REQUEST = 2
    WARNING = 4
    ERROR = 8

class LogAdaptor:

    __cache = {}

    def start_request(self, request):
        request.uid = uuid4().hex
        def request_logger(**kwargs):
            if request.uid not in self.__cache:
                self.__cache[request.uid] = []
            self.__cache[request.uid].append(kwargs)
        request.log = request_logger
        request.log(
            uid=request.uid,
            start_time=time())

    def end_request(self, request):
        request.log(end_time=time())

        # TODO: Asynchronously create log record
        flattened = ChainMap(*self.__cache[request.uid])
        flattened['duration'] = flattened['end_time'] - flattened['start_time']
        print(flattened)

LOG_ADAPTOR = LogAdaptor()
