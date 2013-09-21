#!/usr/bin/env python

import requests
import argparse
import os
import sys
import ConfigParser
import getpass
import errno
import json
import datetime

import exceptions

def retrieve_cached_credentials(url):
    config = ConfigParser.SafeConfigParser()
    auth_file = os.path.expanduser('~/.jira2json/auth')

    config.read(auth_file)

    username = config.get(url, 'username')
    password = config.get(url, 'password')

    return (username, password)

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def write_credentials_to_cache(url,username,password):
    mkdir_p(os.path.expanduser('~/.jira2json'))

    config = ConfigParser.SafeConfigParser()
    auth_file = os.path.expanduser('~/.jira2json/auth')

    config.read(auth_file)

    config.add_section(url)
    config.set(url, 'username', username)
    config.set(url, 'password', password)

    with open(auth_file,'w') as fp:
        config.write(fp)

def ask_credentials_from_stdin(url):
    print "Authentication required to access '%s'" % url

    default_username = getpass.getuser()

    username = raw_input('Username [%s]: ' % default_username)

    if not username:
        username = default_username

    password = getpass.getpass('Password: ')

    return (username, password)

def establish_http_session(username,
                           password,
                           verify_certificate=True):
    session = requests.Session()
    session.verify = verify_certificate
    session.auth = (username, password)

    return session

def get_credentials(url):
    try:
        username,password =\
            retrieve_cached_credentials(url)
    except:
        if not sys.__stdin__.isatty():
            raise Exception("Authentication required")
        
        username, password =\
            ask_credentials_from_stdin(url)

        write_credentials_to_cache(url, username, password)

    return (username, password)


def get_json(session, url, path, params=None):
    full_url = '%s/rest/api/latest/%s' % (url,path)

    r = session.get(full_url, params=params)
    if r.status_code >= 400:
        raise Exception('Failed to access %s' % full_url)


    r_json = json.loads(r.content)
    return r_json

def execute_query(session, url, query, start_at, max_results=10):
    search_params = {
        "jql": query,
        "startAt": start_at,
        "maxResults": max_results,
    }

    return get_json(session, url, 'search', search_params)['issues']
    

def search_issues(session, url, query = ''):
    start_at = 0

    full_query = query

    while True:
        tickets = execute_query(session, url, full_query, start_at)

        if not tickets:
            return

        for ticket in tickets:
            yield ticket

        start_at += len(tickets)

def get_issue(session, url, key):
    return get_json(session, url, 'issue/%s' % key, {})

def compose_query(base_query, days = None):
    since_expr = ''

    if days:
        since_date = datetime.datetime.now() - \
            datetime.timedelta(days = days)
        strtime = '"' + since_date.strftime('%Y/%m/%d %H:%M') + '"'
        since_expr = '( updatedDate > ' + strtime + ' or createdDate > ' + strtime + ')'

    query = '(' + base_query + ')'


    if base_query and since_expr:
        query += ' and '

    if since_expr:
        query += since_expr

    return query

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--days', '-d', type=int)
    parser.add_argument('--query', '-q')
    parser.add_argument('--username', '-u')
    parser.add_argument('--password', '-p')
    parser.add_argument('--no-verify', '-n', action='store_true', default=False)
    parser.add_argument('url', metavar='URL', nargs=1,
                        help='Jira URL')

    args = parser.parse_args()

    url = args.url[0].rstrip('/')

    username = args.username
    password = args.password

    if not args.username:
        username,password = get_credentials(url)
 
    query = compose_query(args.query, args.days)

    session = establish_http_session(username,
                                     password,
                                     args.no_verify)

    first_entry = True
    print '['
    for issue in search_issues(session, url, query):
        if not first_entry:
            print ','

        print get_issue(session, url, issue['key'])
        first_entry = False
    print ']'


if __name__ == '__main__':
    main()
