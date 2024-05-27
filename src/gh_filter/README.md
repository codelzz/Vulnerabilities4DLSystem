## GitHub Vulnerability Filter

`GH Filter` fetch commit/issue/pr information from repositories and store in `raw` folder. Before running `GH Filer`, we need to make sure all repositories are cloned in local machine with proper configuration in `settings.py`

To used it, execute:

```bash
$ python app.py
```

An example output would be:
```bash
[INF] Begin.
[INF] processing tensorflow
[CMD] git log --oneline > <PROJECT_PATH>/src/gh_filer/../../data/raw/tensorflow_commit.csv
[CMD] git log --oneline > <PROJECT_PATH>/src/gh_filer/../../data/raw/tensorflow_pr.csv
[CMD] git log --oneline > <PROJECT_PATH>/src/gh_filer/../../data/raw/tensorflow_issue.csv
[INF] Completed!
```

The `settings.py` file contains the configuration of the program. The available settings include:

* **raw_dir** -  the folder store raw data in .csv format
* **frameworks** - the frameworks we would like to collect
