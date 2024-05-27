## Vulnerability Detector

The `Vuln Detector` applies a latent vulnerability scan based on `Title` and `Description` from Pull Requests. The performance of regular expression for vulnerability keyword searching has been evaluated by official TensorFlow Security Advisory (TFSA) logs. This seach can detected over 98.46% vulnerabilities from the official TFSA.

To used it, execute:

```bash
$ python app.py
```

An example output would be:
```bash
[INF] Begin.
[INF] tensorflow| 1688 vulnerabilities detected.
[INF] pytorch   | 271 vulnerabilities detected.
[INF] opencv    | 677 vulnerabilities detected.
[INF] caffe     | 90 vulnerabilities detected.
[INF] keras     | 83 vulnerabilities detected.
[INF] Completed!
```

The `settings.py` file contains the configuration of the program. The available settings include:

* **distilled_dir** - the folder store extracted data in .csv format.
* **frameworks** - the frameworks we are going to search for vulnerabilities detection.