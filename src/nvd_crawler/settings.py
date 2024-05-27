APP_CONFIG = {
	"distilled_dir":"../../data/distilled/",
	"raw_dir":"../../data/raw/",
    'frameworks': ['tensorflow','caffe','keras','opencv','pytorch'],
    'nvd_search_api': "https://services.nvd.nist.gov/rest/json/cves/1.0?resultsPerPage=2000&keyword=",
    'proxies': {'http': 'http://127.0.0.1:7890','https':'http://127.0.0.1:7890'},
    'headers': {'Accept':'application/vnd.github+json','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',},
}