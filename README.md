# jira2json

Dumps information from Jira issue tracker to json.

Very handy if you want to perform quick-and-dirty analytics that can't be done with default tools.
For instance, correlating ticket updates with certain external events.

## Installation

While this hasn't made it into pypi, you can install it with pip like this:

```
$ pip install -e git+https://github.com/knazarov/jira2json#egg=jira2json
```

The installer will create a 'jira2json' entry point script, which is accessible via $PATH

## Usage

To scrape everything:

```
$ jira2json http://my.jira.local > issues.json
```

Filter using JQL queries:

```
$ jira2json -q 'project = "New office" and status = "open"' http://my.jira.local > issues.json
```

If you are only interested in all open issues created or updated during the last 2 days:

```
$ jira2json -q 'status = "open"' -d 2 http://my.jira.local > issues.json
```


