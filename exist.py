'''
Check if a torrent has already been downloaded
'''
import os
import logging
import glob
from typing import List, Optional

logger = logging.getLogger(__name__)


class Exist:
    '''Check if a torrent has already been downloaded'''

    def __init__(self) -> None:
        pass

    def __call__(
        self,
        tid: str,
        search_dir: Optional[str] = None,
        history: Optional[List[str]] = None
    ) -> bool:
        '''Return True if the torrent has already been downloaded'''
        logger.debug('tid=%s, search_dir=%s', tid, search_dir)

        if history is not None and tid in history:
            return True

        if search_dir is not None:
            # Check for the files on disk recursively
            torrents = glob.glob(
                os.path.join(search_dir, '**', f'{tid}.torrent'),
                recursive=True
            )
            loaded = glob.glob(
                os.path.join(search_dir, '**', f'{tid}.torrent.loaded'),
                recursive=True
            )

            return len(torrents) > 0 or len(loaded) > 0
            
        return False
