from crawler import GHCrawler

import os
import pandas as pd
import requests
import re
import csv

import settings

class CrawlerCommit(GHCrawler):
    """
    CrawlerCommit
    """
    def __init__(self, framework_owner, framework_repo, out_dir, auth, proxies, headers, pr_numbers):
        super(CrawlerCommit, self).__init__(framework_owner=framework_owner, framework_repo=framework_repo, out_dir=out_dir,
            auth=auth, proxies=proxies, headers=headers)
        self.pr_numbers = pr_numbers
        self.commit_fields = ['pr_number', 'sha', 'html', 'message', 'verified', 'verified_reason', 
        				      'line_additions', 'line_deletions', 'changed_files_count', 'changed_files']
        # [Notice] As we only crawled commit for PR with vulnerability information, so the filename of output file
        # will start with `vuln` prefix
        self.commit_csv = self.out_dir + f"vuln_{self.repo}_commit.csv"
        self.prepare()

    def prepare(self):
        self.init_csv(csv_file=self.commit_csv, fields=self.commit_fields)

    def do(self):
        """
        Different from CrawlerPR, Crawler Commit should start from the last pr record (if exist)
        then loop over all pr commits belong it. For each commit belong to the last pr, we then 
        start saving the record from the next of the last commit belong to last pr.
        """
        # get the last save record
        last_crawled_pr_number = self.get_last_pr_number()
        should_crawl_pr = last_crawled_pr_number is None
        # loop over all pr
        for index, pr_number in enumerate(self.pr_numbers):
            # when pr number match the last pr, we start crawling
            if pr_number == last_crawled_pr_number:
                should_crawl_pr = True

            # if should crawl then get the commits related to the PR
            if should_crawl_pr:
                message = f"({index + 1}/{len(self.pr_numbers)}) Crawling commits related to PR {pr_number}:"
                commits = self.get_commits(pr_number=pr_number, message=message)
                # if commits is not valid, skip
                
                if commits is None:
                    continue
                
                # find the last commit related to current pr
                last_crawled_commit_sha = self.get_last_commit_sha_of_pr(pr_number)
                should_crawl_commit = last_crawled_commit_sha is None

                # for each commit 
                for sub_index, commit in enumerate(commits):
                    sha = commit['sha']
                    # if should crawl the commit, we crawl for the detail commit information
                    if should_crawl_commit:
                        message = f"({sub_index + 1}/{len(commits)}) Crawling commit {sha}:"
                        cmt = self.get_commit(sha, message=message)
                        for k, v in cmt.items():
                            commit[k] = v
                            # save the comprehensive commit record
                        self.write_csv(csv_file=self.commit_csv, fields=self.commit_fields, row=commit)
                    else:
                        # if last crawled is not None, we start from the next commmit if matched
                        if last_crawled_commit_sha == sha:
                            should_crawl_commit = True

    def get_commits(self, pr_number, message=None):
        # ref: https://docs.github.com/en/rest/pulls/pulls#get-a-pull-request
        api = self.base_url + f'/pulls/{pr_number}/commits'
        response = self.get(api=api , message=message)
        print('[RSP]',response.status_code,api)
        if response.status_code == 200:
            items = response.json()
            data = []
            for item in items:
                commit = {
                    'pr_number':pr_number,
                    'sha':item['sha'], 
                    'html':item['html_url'], 
                    'message':item['commit']['message'], 
                    'verified':item['commit']['verification']['verified'], 
                    'verified_reason':item['commit']['verification']['reason']
                }
                data.append(commit)
            return data

    def get_commit(self, sha, message=None):
        api = self.base_url + f'/commits/{sha}'
        response = self.get(api=api , message=message)

        if response.status_code == 200:
            item = response.json()
            data = {
                'line_additions':item['stats']['additions'],
                'line_deletions':item['stats']['deletions'],
                'changed_files_count':len(item['files']), 
                'changed_files': [file['filename'] for file in item['files']],
            }
            return data


    def get_last_pr_number(self):
        df = pd.read_csv(self.commit_csv)
        if len(df.index) > 0:
            return df.iloc[-1]['pr_number']

    def get_last_commit_sha_of_pr(self, pr_number):
        df = pd.read_csv(self.commit_csv)
        df = df[df['pr_number'] == pr_number]
        if len(df.index) > 0:
            return df.iloc[-1]['sha']


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
    #PROXIES       = settings.APP_CONFIG['proxies'] # support proxy
    #
    FRAMEWORKS    = settings.APP_CONFIG['frameworks']

    for owner, repo in FRAMEWORKS.items():
        vuln_pr_file = DISTILLED_DIR + f'vuln_{repo}_pr.csv'
        df = pd.read_csv(vuln_pr_file)
        pr_numbers = list(df['number'])
        pr_numbers.sort(reverse=True)
        crawler = CrawlerCommit(
            framework_owner=owner, 
            framework_repo=repo, 
            out_dir=DISTILLED_DIR, 
            auth=AUTH,
            proxies=PROXIES, 
            headers=HEADERS,
            pr_numbers=pr_numbers)
        crawler.do()

    print("[INF] End.")
