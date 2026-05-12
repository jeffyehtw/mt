'''
Download torrent files from M-Team
'''
from typing import Dict, Optional, Tuple
import os
import json
import requests
import logging

from mt.base import BASE_URL, post

logger = logging.getLogger(__name__)


class Download:
    '''Download a torrent file from M-Team'''

    def __init__(self, key: str) -> None:
        '''Initialize with API key'''
        self.key = key

    def __call__(
        self,
        tid: str,
        local_dir: str,
        detail: Dict = None
    ) -> Tuple[Optional[str], Optional[str]]:
        '''Download torrent by ID to local_dir. Returns (file_path, url).'''
        logger.debug('tid=%s, local_dir=%s', tid, local_dir)

        try:
            # Step 1: Get a temporary download token/URL from the API
            data = post(
                self.key,
                f'{BASE_URL}/torrent/genDlToken',
                {'id': tid},
                form=True
            )
            if data is None:
                logger.info('action=skip, reason=!data')
                return None, None

            # Step 2: Append connection options and fetch torrent file
            torrent_url = data + '&useHttps=true&type=ipv4'
            response = requests.get(torrent_url, timeout=30)

            if response.status_code != 200:
                logger.info(
                    'action=skip, reason=!response, status=%s',
                    response.status_code
                )
                return None, None

            # Check if it's a JSON error message instead of a torrent file
            if response.content.startswith(b'{"code":'):
                try:
                    error_data = response.json()
                    if error_data.get('message'):
                        logger.error(
                            'action=download_fail, reason=%s',
                            error_data['message']
                        )
                        return None, None
                except Exception:
                    pass

            # Step 3: Save the .torrent file
            logger.info('action=download, tid=%s, dir=%s', tid, local_dir)
            os.makedirs(local_dir, exist_ok=True)
            torrent_path = os.path.join(local_dir, f'{tid}.torrent')
            with open(torrent_path, 'wb') as fp:
                fp.write(response.content)

            # Step 4: Optionally save torrent metadata as a .info file
            if detail is not None:
                info_path = os.path.join(local_dir, f'{tid}.info')
                with open(info_path, 'w') as fp:
                    json.dump(detail, fp, indent=4)

            return torrent_path, torrent_url

        except Exception as e:
            logger.error(str(e))
        
        return None, None
