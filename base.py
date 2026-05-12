'''
Shared HTTP helpers for M-Team API requests
'''
from typing import Dict
import time
import random
import requests
import logging

from utils import MTeamAPIError

logger = logging.getLogger(__name__)

BASE_URL = 'https://api.m-team.cc/api'

def headers(key: str) -> Dict:
    '''Return common API request headers'''
    return {'x-api-key': key}

def post(key: str, url: str, payload: Dict, form: bool = False) -> Dict:
    '''Send a POST request with a random delay to avoid rate limiting'''
    logger.debug('url=%s, payload=%s, form=%s', url, payload, form)

    time.sleep(random.randint(2, 5))

    # Endpoints that expect form-encoded data (detail, download)
    if form:
        response = requests.post(
            url,
            headers=headers(key),
            data=payload,
            timeout=30
        )
    # Endpoints that accept JSON (search)
    else:
        response = requests.post(
            url,
            headers=headers(key),
            json=payload,
            timeout=30
        )

    if response.status_code != 200:
        logger.error(
            'action=post, reason=!response, status=%s',
            response.status_code
        )
        raise MTeamAPIError(
            f'M-Team API request failed with status {response.status_code}'
        )

    ret = response.json()
    if ret.get('message') != 'SUCCESS':
        error_msg = ret.get('message')
        logger.error('action=post, reason=%s', error_msg)
        raise MTeamAPIError(f'M-Team API error: {error_msg}')

    return ret.get('data')

