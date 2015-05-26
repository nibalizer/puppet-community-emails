#!/usr/bin/env python

import json
from github import Github
from datetime import datetime, timedelta
import config

def totimestamp(dt, epoch=datetime(1970,1,1)):
    td = dt - epoch
    # return td.total_seconds()
    return int((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1e6 )


if __name__ == "__main__":

    g = Github(config.token)
    pc = g.get_organization('puppet-community')

    # embarassing that we can't ask this
    total_issues = 0
    total_prs = 0
    repo_most_issues = ("repo", 0)
    repo_most_prs = ("repo", 0)
    for repo in pc.get_repos():
        #from pdb import set_trace; set_trace()
        #print repo.name
        pr_count = 0
        for pr  in repo.get_pulls():
            #print pr.number
            pr_count += 1
        issues = repo.open_issues - pr_count
        total_issues += issues
        total_prs += pr_count
        rmi = repo_most_issues[1]
        if issues > rmi:
            repo_most_issues = (repo, issues)
        rmp = repo_most_issues[1]
        if pr_count > rmp:
            repo_most_prs = (repo, pr_count)



    print "Total Issues: %s" % total_issues
    print "Total Pull Requests: %s" % total_prs
    print "Repo with the most open issues: %s with %s issues" % (repo_most_issues[0].name, repo_most_issues[1])
    print "Repo with the most open prs: %s with %s prs" % (repo_most_prs[0].name, repo_most_prs[1])



