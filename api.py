import typing
'''
M-Team torrent tracker API wrapper
'''
import logging

from mt.latest import Latest
from mt.download import Download
from mt.exist import Exist
from mt.detail import Detail
from mt.search import Search

logger = logging.getLogger(__name__)

class MT:
    '''Client for the M-Team torrent tracker API'''

    def __init__(
        self,
        rss: str = None,
        key: str = None,
    ) -> None:
        '''Initialize the MT client and its sub-operation instances'''
        logger.debug('rss=%s', rss)

        self.key = key
        self.rss = rss

        self.latest = Latest(key=key, rss=rss)
        self.download = Download(key=key)
        self.exist = Exist()
        self.detail = Detail(key=key)
        self.search = Search(key=key)

    def __enter__(self) -> "MT":
        return self

    def __exit__(
        self,
        exc_type: typing.Any,
        exc_value: typing.Any,
        traceback: typing.Any
    ) -> None:
        pass
