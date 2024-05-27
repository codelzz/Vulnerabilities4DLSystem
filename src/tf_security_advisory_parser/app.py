#coding=utf-8
import os
import pandas as pd
import re
from bs4 import BeautifulSoup
import markdown
import settings

def parsing_md_file(f):
    file = open(f, errors='ignore')
    lines = [line for line in file.readlines() if line.strip()]
    data = []
    for line in lines:
        data.append(re.split('\n', line)[0]) #provide more general splitter
    dic = {}
    
    key0, value0 = data[0].split(': ')
    dic['TFSA']=value0
    data = data[1:]
    key_index = []
    for i in data:
        if '### ' in i:
            key_index.append(data.index(i))
    for i in range(len(key_index)):
        key = data[key_index[i]].strip("### ")
        if i < len(key_index) - 1:
            value = ''
            for j in range(key_index[i],key_index[i+1]-1):
                value = " ".join((value,data[j+1]))
            dic[key]=value
        if i == len(key_index) - 1:
            value = ''
            for j in range(key_index[i]+1,len(data)):
                value = " ".join((value, data[j]))
            dic[key]=value
    return dic

def get_md_files(raw_dir):
    os_dir = os.walk(raw_dir)
    files = []
    for path, dir_list, file_list in os_dir:
        for file_name in file_list:
            files.append("".join((path,file_name)))
    return files

def extract_data(files):
    data = {"TFSA":[],"CVE Number":[],"Patches":[],"Issue Description":[],"Impact":[],"Vulnerable Versions":[],"Mitigation":[],"Credits":[],"Attribution":[]}
    total_file_num = len(files)
    for i, file in enumerate(files):
        print(f"[INF] ({i+1}/{total_file_num}) Extracting data from {file.split('/')[-1]}")
        parsed_data = parsing_md_file(file)
        for k in parsed_data:
            if k in data:
                data[k].append(parsed_data[k])
        for k in data:
            if k not in parsed_data:
                data[k].append("None")  
    return data


if __name__ == "__main__":
    print("[INF] Begin.")

    RAW_DIR       = settings.APP_CONFIG['raw_dir']
    DISTILLED_DIR = settings.APP_CONFIG['distilled_dir']
    OUTPUT_FILE   = DISTILLED_DIR + settings.APP_CONFIG['output_file']

    # Get and extract data from md files
    get_md_files = get_md_files(raw_dir=RAW_DIR)
    data = extract_data(files=get_md_files)

    # Save extract data to output file
    df = pd.DataFrame(data)#, index=[0]).T
    df.to_csv(OUTPUT_FILE,index=False)
    
    print("[INF] Completed!")