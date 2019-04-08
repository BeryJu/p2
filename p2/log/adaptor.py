"""p2 logging"""
from collections import ChainMap
from time import time
from uuid import uuid4


class LogAdaptor:
    """Cache logged data and add log method to request"""

    __cache = {}

    def start_request(self, request):
        """Add unique ID to request and create logging method"""
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
        """Flatten logged data and create Record"""
        request.log(end_time=time())

        # TODO: Asynchronously create log record
        flattened = ChainMap(*self.__cache[request.uid])
        flattened['duration'] = flattened['end_time'] - flattened['start_time']
        print(flattened)

LOG_ADAPTOR = LogAdaptor()
