
## 
# print text by matched keyword
# 
# use for manually check the search result
def df_col_by_keyword(df, keyword, search_col_name, info_col_name, n=5):
    i = 0
    for index, value in df[df[search_col_name] == keyword][info_col_name].items():
        if i > n - 1:
            break
        print(index,'\t',value)
        i+=1
    print(f"Total:{i}")

## 
# print text by column names
# 
# use for manually check the search result
def df_cols(df, col_names, n=5):
    i = 0
    for index, row in df.iterrows():
        if i > n - 1:
            break
        print(index,'\t', '\t'.join([row[col_name] for col_name in col_names]))
        i+=1
    print(f"Total:{i}")