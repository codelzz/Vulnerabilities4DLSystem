## TensorFlow Security Advisory Parser

The TFSecurityAdvisory can manually [download](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/security/advisory) from TensorFlow. Here, we already download them and save to `data\raw\securiy_advisory_tensorflow` directory.
 
`TFSecurityAdvisoryParser` can can extract data from `Security Advisory` files and clean them up.

To used it, execute:

```bash
$ python app.py
```

An example output would be:
```bash
[INF] Begin.
...
[INF] (317/326) Extracting data from tfsa-2021-120.md
[INF] (318/326) Extracting data from tfsa-2021-060.md
[INF] (319/326) Extracting data from tfsa-2021-093.md
[INF] (320/326) Extracting data from tfsa-2021-182.md
[INF] (321/326) Extracting data from tfsa-2021-054.md
[INF] (322/326) Extracting data from tfsa-2021-114.md
[INF] (323/326) Extracting data from tfsa-2021-005.md
[INF] (324/326) Extracting data from tfsa-2021-145.md
[INF] (325/326) Extracting data from tfsa-2022-079.md
[INF] (326/326) Extracting data from tfsa-2022-028.md
[INF] Completed!
```

The `settings.py` file contains the configuration of the program. The available settings include:

* **output_file** - the name of extract file
* **distilled_dir** - the folder store extracted data in .csv format
* **raw_dir** -  the folder store raw data in .md format