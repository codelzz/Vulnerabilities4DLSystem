import os
import numpy as np
import pandas as pd
import re
import random
import settings
from searchkey import VulnerabilityRegex
import platform


def latent_vuln_detection(df):
    vuln_re = VulnerabilityRegex.basic() + '|' + VulnerabilityRegex.enhence()
    # search vulnerability keyword from `Title`
    df['title keyword'] = df['title'].str.extract(f"({vuln_re})", flags=re.IGNORECASE)[0].str.lower()
    # search vulnerability keyword from `Description`
    df['description keyword'] = df['description'].str.extract(f"({vuln_re})", flags=re.IGNORECASE)[0].str.lower()
    # get vulnerable mask
    mask = ~df['title keyword'].isnull() | ~df['description keyword'].isnull()
    vuln_df = df[mask].reset_index(drop=True)
    # normalize keywords from `Title`
    vuln_df['title keyword'] = VulnerabilityRegex.normalize_enhence_searchkey(vuln_df['title keyword'])
    vuln_df['title keyword'] = VulnerabilityRegex.normalize_searchkey(vuln_df['title keyword'])
    # normalize keywords from `Description`
    vuln_df['description keyword'] = VulnerabilityRegex.normalize_enhence_searchkey(vuln_df['description keyword'])
    vuln_df['description keyword'] = VulnerabilityRegex.normalize_searchkey(vuln_df['description keyword'])
    return vuln_df

if __name__ == "__main__":
    print("[INF] Begin.")
    DISTILLED_DIR = settings.APP_CONFIG['distilled_dir']
    FRAMEWORKS    = settings.APP_CONFIG['frameworks']

    for owner, repo in FRAMEWORKS.items():
        merged_pr_file = DISTILLED_DIR + f'merged_{repo}_pr.csv'
        vuln_pr_file = DISTILLED_DIR + f'vuln_{repo}_pr.csv'

        # fix platform encoding issue
        encoding = 'latin1'         # for windows
        if platform.system() == 'Darwin': 
            encoding='iso-88591-1'  # for mac os

        vuln_pr_df = latent_vuln_detection(df=pd.read_csv(merged_pr_file, encoding=encoding))
        vuln_pr_df.to_csv(vuln_pr_file, index=False)
        print(f"[INF] {repo:10}| {len(vuln_pr_df)} vulnerabilities detected.")

    print("[INF] Completed!")