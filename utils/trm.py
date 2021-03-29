#!/usr/bin/env python
import json
import requests


def get_trm():
    r = requests.get('https://s3.amazonaws.com/dolartoday/data.json')
    data = json.loads(r.text)
    return data['USDCOL']['ratetrm']
