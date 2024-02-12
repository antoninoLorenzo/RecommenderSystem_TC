"""
Startup TC Recommender AI
"""
import os
import sys
import argparse

try:
    import fastapi
    import uvicorn
    import sqlalchemy
    import pymysql
    import pydantic

    import numpy
    import pandas
    import scipy
    import sklearn
    import nltk
    import langdetect

    import matplotlib
    import seaborn
    import folium

    import exrex
    import faker
    import requests
except ImportError as import_err:
    print(f'[!] ImportError: {import_err}')
    sys.exit(1)


PARSER = argparse.ArgumentParser(
    prog='TC Recommender API',
    description=''
)
PARSER.add_argument('-A', '--address', required=True)
PARSER.add_argument('-U', '--user', required=True)
PARSER.add_argument('-P', '--password', required=True)


if __name__ == "__main__":
    args = PARSER.parse_args()
    try:
        config = {
            'host': args.address.split(':')[0],
            'port': args.address.split(':')[1].split('/')[0],
            'connection': args.address.split(':')[1].split('/')[1],
            'usr': args.user,
            'psw': args.password
        }
    except IndexError:
        print('[!] Invalid format for address')
        sys.exit(1)

    os.environ.setdefault('DB_USR', config['usr'])
    os.environ.setdefault('DB_PSW', config['psw'])
    os.environ.setdefault('DB_HOST', config['host'])
    os.environ.setdefault('DB_PORT', config['port'])
    os.environ.setdefault('DB_CONN', config['connection'])

    import src.presentation.api as recommender_api
    recommender_api.launch()
