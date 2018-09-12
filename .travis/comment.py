#! /usr/bin/env python
import os
import sys
import json
import requests

def comment_on_pull_request(pr_number,slug, token, comment):
    url = 'https://api.github.com/repos/{slug}/issues/{number}/comments'.format(
        slug=slug, number=pr_number)
    response = requests.post(url, data=json.dumps({'body': comment}),
        headers={'Authorization': 'token ' + token})
    return response.json()

if __name__ == '__main__':
    print "start post"
    PR_NUMBER = os.environ.get('TRAVIS_PULL_REQUEST')
    REPO_SLUG = os.environ.get('TRAVIS_REPO_SLUG')
    TOKEN = os.environ.get('GH_TOKEN')
    results = "test"
    print PR_NUMBER
    print REPO_SLUG
    print TOKEN
    '''PR_NUMBER = 1
    REPO_SLUG = "learn_python"
    TOKEN = "ef703762fe300bdcbf4676b91178c16d9396a2e7"
    USER = "wangnuannuan"'''
    
    comment = "```{flake_results}```".format(flake_results=results)
    
    if all([PR_NUMBER, REPO_SLUG, TOKEN, results.strip()]):
        print comment_on_pull_request(PR_NUMBER, REPO_SLUG, TOKEN, comment)