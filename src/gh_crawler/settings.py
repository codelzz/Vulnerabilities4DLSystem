APP_CONFIG = {
	'auth':('<GITHUB_ACCOUNT>','<TOKEN>'),
	'proxies': {'http': 'http://127.0.0.1:7890','https':'http://127.0.0.1:7890'},
	'headers': {
				'Accept':'application/vnd.github+json',
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
				},
	"distilled_dir":"../../data/distilled/",
	"raw_dir":"../../data/raw/",
	'frameworks':{
		'tensorflow':'tensorflow',
		'pytorch':'pytorch',
		'opencv':'opencv',
		'BVLC':'caffe',
		'keras-team':'keras',
		},
}