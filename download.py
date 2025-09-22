import os
import sys
import json
import logging
import argparse

__description__ = ''
__epilog__ = 'Report bugs to <yehcj.tw@gmail.com>'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

from modules.mt import MT

def load(file: str) -> dict:
    config = None
    if not os.path.exists(file):
        return config
    with open(file, 'r') as fp:
        config = json.load(fp)
    return config

def main():
    parser = argparse.ArgumentParser(
        description=__description__,
        epilog=__epilog__
    )
    parser.add_argument('--id', type=str, nargs='+', required=True, default=[])
    parser.add_argument('--key', type=str, default=None)
    parser.add_argument('--output', type=str, default=None)
    parser.add_argument('--verbose', action='store_true', default=False)

    args = parser.parse_args(sys.argv[1:])

    # load configuration file
    config = load(os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'mt.json'
    ))

    # # overwrite the configuration if a parameter is provided
    if args.key is None:
        args.key = config['key']
    if args.output is None:
        args.output = config['output']

    with MT(key=args.key, output=args.output) as mt:
        for tid in args.id:
            logging.info(f'tid={tid}')
            if args.verbose:
                detail = mt.detail(tid=tid)
                logging.info('status=%s', detail['status']['discount'])
                logging.info('name=%s', detail['name'])
            mt.download(tid=tid)

if __name__ == '__main__':
    main()
