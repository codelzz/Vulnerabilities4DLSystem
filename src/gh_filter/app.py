#coding=utf-8
import os
import pandas as pd
import subprocess
import settings


class GHFilter:
    def __init__(self, raw_dir):
        self.origin_pwd = os.getcwd()
        self.raw_dir = raw_dir
        self.fetch_limit = 1000000

    def process(self, framework, path):
        print(f'[INF] processing {framework}')
        os.chdir(path)

        ## fetch commits
        self.fetch_commit(framework=framework)
        ## fetch issues
        self.fetch_issue(framework=framework)
        ## fetch pr
        self.fetch_pr(framework=framework)

        # reset pwd for next round
        os.chdir(self.origin_pwd)

    def fetch_commit(self, framework):
        raw = self.get_raw_file(framework, tag='commit')
        cmd = f'git log --oneline > {raw}'
        print('[CMD] ' + cmd)
        os.system(cmd)

    def fetch_issue(self, framework):
         self.fetch(framework=framework, tag='issue')

    def fetch_pr(self, framework):
        self.fetch(framework=framework, tag='pr')

    def fetch(self, framework, tag):
        raw = self.get_raw_file(framework=framework, tag=tag)
        cmd = f'gh {tag} list --limit {self.fetch_limit} --state all | tr "\t" "," > {raw}'
        print('[CMD] ' + cmd)
        os.system(cmd)

    def get_raw_file(self, framework, tag):
        return f'{self.origin_pwd+"/"+self.raw_dir + framework + "_" + tag}.csv'


if __name__ == "__main__":
    print("[INF] Begin.")

    # Load global setting
    RAW_DIR    = settings.APP_CONFIG['raw_dir']
    FRAMEWORKS = settings.DATA_CONFIG['frameworks']

    gh_filter = GHFilter(raw_dir=RAW_DIR)

    # for each framework run gh command respectively
    for framework in FRAMEWORKS:
        repo_key = framework + '_repo'
        if repo_key not in  settings.DATA_CONFIG.keys():
            print(f'[WAN] {framework} local repository not specified.')
            continue
        else:
            path = settings.DATA_CONFIG[repo_key]
            gh_filter.process(framework=framework, path=path)
    
    print("[INF] Completed!")