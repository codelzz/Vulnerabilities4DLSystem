
import os
import pandas as pd
import requests
import re
import csv

import settings

class GHCrawler:
    """ 
    GHCrawler

    Crawl deep learning framework github by given repository
    """
    # Crawler Routine
    def __init__(self, framework_owner, framework_repo, out_dir, auth=None, proxies={}, headers={'Accept':'application/vnd.github+json'}):
        self.owner = framework_owner        # the ower of the framework
        self.repo = framework_repo          # the name of the framework
        self.out_dir = out_dir              # the directory where output file located
        self.auth = auth                    # the authentication info for API
        self.session = requests.Session()   # the session with authentication information for API calls
        self.session.auth = self.auth       
        self.proxies = proxies              # the local proxy for VPN
        self.headers = headers              # the header in output file
        self.base_url =  r'https://api.github.com/repos/' + f'{self.owner}/{self.repo}'
        
    @staticmethod 
    def init_csv(csv_file, fields):
        '''
        If output file not exist, then create a new file with corresponding field (header)
        '''
        if not os.path.exists(csv_file):
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                w = csv.DictWriter(f, fieldnames=fields)
                w.writeheader()
                f.close()

    @staticmethod
    def write_csv(csv_file, fields, row):
        '''
        open the output file and add a row to the end of file
        '''
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writerow(row)
            f.close()

    def do(self):
        '''virtual method'''
        pass

    def get(self, api, message=None):
        ''' debug get method, print out the API call on console'''
        print("[GET] " + message + " " + api)
        return self.session.get(api, auth=self.auth, proxies=self.proxies, headers=self.headers)