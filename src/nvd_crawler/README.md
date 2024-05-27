## NVD Crawler

`NVD Crawler` query the [NVD](https://nvd.nist.gov/vuln/search) database by given keywords. It cache the raw json data in `raw` folder then parse it as csv in `distilled` folder.

To used it, execute:

```bash
$ python app.py
```

An example output would be:
```bash
[INF] Begin.
[GET] tensorflow| https://services.nvd.nist.gov/rest/json/cves/1.0?resultsPerPage=2000&keyword=tensorflow
[GET] caffe     | https://services.nvd.nist.gov/rest/json/cves/1.0?resultsPerPage=2000&keyword=caffe
[GET] keras     | https://services.nvd.nist.gov/rest/json/cves/1.0?resultsPerPage=2000&keyword=keras
[GET] opencv    | https://services.nvd.nist.gov/rest/json/cves/1.0?resultsPerPage=2000&keyword=opencv
[GET] pytorch   | https://services.nvd.nist.gov/rest/json/cves/1.0?resultsPerPage=2000&keyword=pytorch
[INF] Completed!
```

The `settings.py` file contains the configuration of the program. The available settings include:

* **frameworks** - the framework we are going to search in NVD database
* **nvd_search_api** - the api for query
* **distilled_dir** - the folder store parsed data in .csv format
* **raw_dir** -  the folder store raw data in .json format