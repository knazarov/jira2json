# jira2json

Dumps information from Jira issue tracker to json.

Very handy if you want to perform quick-and-dirty analytics that can't be done with default tools.
For instance, correlating ticket updates with certain external events.

## Usage

To scrape everything:

```
$ ./jira2json.py http://my.jira.local > issues.json
```

Filter using JQL queries:

```
$ ./jira2json.py -q 'project = "New office" and status = "open"' http://my.jira.local > issues.json
```

If you are only interested in all open issues created or updated during the last 2 days:

```
$ ./jira2json.py -q 'status = "open"' -d 2 http://my.jira.local > issues.json
```


