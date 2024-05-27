import os
import settings
import requests
import json
import time
import pandas as pd
import numpy as np

from utils import JSONParser

def cache_raw_data(framework, raw_dir, search_api, proxies=None):
    api = search_api + framework
    print(f"[GET] {framework:10}| {api}")
    r = requests.get(api, proxies=proxies)
    if r.status_code != 200:
        return -1
    output = raw_dir + f'nvd_{framework}.json'
    
    with open(output, 'w') as f:
        data = r.json()
        json.dump(data, f)
        f.close()
        return data['totalResults']

def parse_raw_data(framework, raw_dir, distilled_dir):
    parser = JSONParser(raw_dir=raw_dir, distilled_dir=distilled_dir)
    parser.parse(framework=framework)

if __name__ == "__main__":
    print("[INF] Begin.")
    # Load configuration
    DISTILLED_DIR   = settings.APP_CONFIG['distilled_dir']
    RAW_DIR         = settings.APP_CONFIG['raw_dir']
    FRAMEWORKS      = settings.APP_CONFIG['frameworks']
    NVD_SEARCH_API  = settings.APP_CONFIG['nvd_search_api']
    PROXY           = None
    #PROXY           = settings.APP_CONFIG['proxies'] # Support Proxy

    for framework in FRAMEWORKS:
        num = cache_raw_data(framework=framework, raw_dir=RAW_DIR, search_api=NVD_SEARCH_API, proxies=PROXY)
        parse_raw_data(framework=framework, raw_dir=RAW_DIR, distilled_dir=DISTILLED_DIR)
        time.sleep(1)

    print("[INF] Completed!")