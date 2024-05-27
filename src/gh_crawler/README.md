## GitHub Crawler

`GH Crawler` will crawl GitHub data via [GitHub REST API](`https://docs.github.com/en/rest`).

To maximise the crawler performance, you need configure the `auth` parameter in `setting.py` with user account and corresponding token. Otherwise, you can only perform 50 API calls per hour. With authentication token, this limitation will increase to 5000 API per hours.

To used it, execute:

For crawling PR information
```bash
$ python crawler_pr.py
```

An example output would be:
```bash
[INF] Begin.
[GET] (1/2663) Crawling PR 16778: https://api.github.com/repos/keras-team/keras/pulls/16778
[GET] (2/2663) Crawling PR 16772: https://api.github.com/repos/keras-team/keras/pulls/16772
[GET] (3/2663) Crawling PR 16767: https://api.github.com/repos/keras-team/keras/pulls/16767
[GET] (4/2663) Crawling PR 16765: https://api.github.com/repos/keras-team/keras/pulls/16765
...
[INF] Completed!
```

Notice: Before start crawling the commit, we need to first perform the latent vulnerability search on PR records and generated the corresponding vulnerability pr file. The commit crawler will fetch the commits record according to the vulnerable PR results.

For crawling corresponding Commits
```bash
$ python crawler_commit.py
```

An example output would be:
```bash
[INF] Begin.
...
[GET] (1665/1665) Crawling commits related to PR 673: https://api.github.com/repos/tensorflow/tensorflow/pulls/673/commits
[GET] (270/270) Crawling commits related to PR 52: https://api.github.com/repos/pytorch/pytorch/pulls/52/commits
[GET] (677/677) Crawling commits related to PR 14: https://api.github.com/repos/opencv/opencv/pulls/14/commits
[GET] (83/83) Crawling commits related to PR 19: https://api.github.com/repos/keras-team/keras/pulls/19/commits
...
[INF] Completed!
```
