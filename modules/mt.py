import os
import json
import time
import random
import shutil
import requests
import xmltodict
import logging

class Url():
    def __init__(self):
        self.detail = 'https://api.m-team.cc/api/torrent/detail'
        self.download = 'https://api.m-team.cc/api/torrent/genDlToken'
        self.search = 'https://api.m-team.cc/api/torrent/search'

class MT():
    def __init__(self, rss: str = None, key: str = None, output: str = None):
        self.key = key
        self.rss = rss
        self.output = output
        self.url = Url()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def latest(self) -> list[dict]:
        try:
            response = requests.get(self.rss, headers={ 'x-api-key': self.key })
            if response.status_code == 200:
                ret = xmltodict.parse(response.text, attr_prefix='')
                return ret['rss']['channel']['item']
            else:
                logging.error('Request failed')
        except Exception as e:
            logging.error(str(e))
        return None

    def download(self, tid: str) -> None:
        headers = { 'x-api-key': self.key }
        payload = { 'id': tid }

        try:
            time.sleep(random.randint(2, 5))
            response = requests.request(
                'POST',
                self.url.download,
                headers=headers,
                data=payload
            )
            if response.status_code == 200:
                response = response.json()
                if response['message'] == 'SUCCESS':
                    url = response['data'] + '&useHttps=true&type=ipv4'

                    response = requests.get(url)
                    if response.status_code == 200:
                        if not self.exist(tid):
                            logging.info('Download')
                            torrent = os.path.join(self.output, f'{tid}.torrent')
                            with open(torrent, 'wb') as fp:
                                fp.write(response.content)
                        else:
                            logging.info('Exist')
                    else:
                        logging.error('Download failed')
            else:
                logging.error('Request failed')

        except Exception as e:
            logging.error(str(e))

    def exist(self, tid: str) -> bool:
        torrent = os.path.join(self.output, f'{tid}.torrent')
        synology = os.path.join(self.output, f'{tid}.torrent.loaded')
        return os.path.exists(torrent) or os.path.exists(synology)

    def detail(self, tid: str) -> dict:
        payload = { 'id': tid }
        headers = { 'x-api-key': self.key }

        try:
            time.sleep(random.randint(2, 5))
            response = requests.request(
                'POST',
                self.url.detail,
                headers=headers,
                data=payload
            )
            if response.status_code == 200:
                ret = response.json()
                if ret['message'] == 'SUCCESS':
                    return ret['data']
                else:
                    logging.error('Request failed')
            else:
                logging.error('Request failed')
        except Exception as e:
            logging.error(str(e))

        return None

    def search(
            self,
            mode: str,
            free: bool,
            index: int,
            size: int,
            keyword: str
        ) -> list[dict]:
        headers = { 'x-api-key': self.key }
        payload = {
            'mode': mode,
            'pageNumber': index,
            'pageSize': size,
        }

        if free:
            payload['discount'] = 'FREE'
        if keyword is not None:
            payload['keyword'] = keyword

        try:
            time.sleep(random.randint(2, 5))
            response = requests.post(
                self.url.search,
                headers=headers,
                json=payload
            )
            if response.status_code == 200:
                return response.json()['data']['data']
            else:
                logging.error('Request failed')

        except Exception as e:
            logging.error('Request failed')
