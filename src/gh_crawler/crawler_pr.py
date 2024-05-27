from crawler import GHCrawler
import platform
import os
import pandas as pd
import requests
import re
import csv

import settings

class CrawlerPR(GHCrawler):
    def __init__(self, 
        framework_owner, 
        framework_repo, 
        out_dir, 
        auth, 
        proxies, 
        headers, 
        pr_numbers):
        super().__init__(
            framework_owner=framework_owner, 
            framework_repo=framework_repo, 
            out_dir=out_dir,
            auth=auth, 
            proxies=proxies, 
            headers=headers)
        self.pr_numbers = pr_numbers
        self.pr_fields = ['number', 'html', 'title', 'description', 
                          'comments_count', 'review_comments_count', 'commits_count', 
                          'line_additions', 'line_deletions', 'changed_files_count', 
                          'created_at','updated_at','closed_at', 'merged_at']
        self.pr_csv = self.out_dir + f"merged_{self.repo}_pr.csv"
        self.prepare()

    def prepare(self):
        self.init_csv(csv_file=self.pr_csv, fields=self.pr_fields)

    def do(self):
        last_crawled_pr_number = self.get_last_pr_number()
        should_crawl = last_crawled_pr_number is None
        for index, pr_number in enumerate(self.pr_numbers):
            if should_crawl:
                message = f"({index + 1}/{len(self.pr_numbers)}) Crawling PR {pr_number}:"
                pr = self.get_pull_request(pr_number=pr_number, message=message)
                self.write_csv(csv_file=self.pr_csv, fields=self.pr_fields, row=pr)
            else:
                if pr_number == last_crawled_pr_number:
                    should_crawl = True

    def get_pull_request(self, pr_number, message=None):
        # ref: https://docs.github.com/en/rest/pulls/pulls#get-a-pull-request
        api = self.base_url + f'/pulls/{pr_number}'
        response = self.get(api=api , message=message)
        print('[RSP]',response.status_code, api)
        if response.status_code == 200:
            item = response.json()
            data = {
                'number':item['number'],
                'html':item['html_url'],
                'title': item['title'],
                'description': item['body'],
                'comments_count': item['comments'],
                'review_comments_count': item['review_comments'],
                'commits_count': item['commits'],
                'line_additions': item['additions'],
                'line_deletions': item['deletions'],
                'changed_files_count': item['changed_files'],
                'created_at':item['created_at'],
                'updated_at':item['updated_at'],
                'closed_at':item['closed_at'], 
                'merged_at':item['merged_at'],
            }
            return data

    def get_last_pr_number(self):
        encoding = 'latin1'         # for windows
        if platform.system() == 'Darwin': 
            encoding='iso-88591-1'  # for mac os
        df = pd.read_csv(self.pr_csv, encoding=encoding)
        if len(df.index) > 0:
            return df.iloc[-1]['number']


def read_raw_pr_with_merge(raw_pr_file):
    # Regex
    REGEX_ONLY_FIRST_COMMA = "^([^,]*)," 
    REGEX_AFTER_LAST_COMMA = "[^,]*$"
    REGEX_BEFORE_LAST_COMMA = '.+(?=,)'
    # Formating: isolate pr_number, status, and description
    df = pd.read_csv(raw_pr_file, sep=REGEX_ONLY_FIRST_COMMA, engine='python', header=0, names=["tmp", "pr_number","description"]).drop(columns=["tmp"])
    df['status']      = df['description'].str.extract(f"({REGEX_AFTER_LAST_COMMA})", flags=re.IGNORECASE)
    df['description'] = df['description'].str.extract(f"({REGEX_BEFORE_LAST_COMMA})", flags=re.IGNORECASE)
    # Filtering : only key status with merged
    df = df[df['status'] == 'MERGED'].reset_index(drop=True)
    return df

if __name__ == "__main__":
    print("[INF] Begin.")

    DISTILLED_DIR = settings.APP_CONFIG['distilled_dir']
    RAW_DIR       = settings.APP_CONFIG['raw_dir']
    #
    AUTH          = settings.APP_CONFIG['auth']
    HEADERS       = settings.APP_CONFIG['headers']
    PROXIES       = None
    # PROXIES       = settings.APP_CONFIG['proxies'] # support proxy
    #
    FRAMEWORKS = settings.APP_CONFIG['frameworks']

    for owner, repo in FRAMEWORKS.items():
        '''
        the data from GHVFilter are gattered by gh command.
        We use github web API to crawl the github again because
        it provide much more detial information
        '''
        raw_pr_file = RAW_DIR + f'{repo}_pr.csv'
        df = read_raw_pr_with_merge(raw_pr_file)
        pr_numbers = list(df['pr_number'])
        pr_numbers.sort(reverse=True)
        crawler = CrawlerPR(framework_owner=owner, 
                            framework_repo=repo, 
                            out_dir=DISTILLED_DIR, 
                            auth=AUTH,
                            proxies=PROXIES, 
                            headers=HEADERS,
                            pr_numbers=pr_numbers)
        crawler.do()

    print("[INF] End.")
