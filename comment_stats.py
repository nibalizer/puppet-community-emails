#!/usr/bin/env python

import json
from github import Github
from datetime import datetime, timedelta
import config

from pdb import set_trace
from collections import defaultdict

def totimestamp(dt, epoch=datetime(1970,1,1)):
    td = dt - epoch
    # return td.total_seconds()
    return int((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1e6 )

def before(date, days=30):
    if date < (datetime.now() - timedelta(30)):
        return False
    else:
        return True

user_actions = {}

def user_action(user, action):
    if user is None:
        return
    if user not in user_actions.keys():
        user_actions[user] = {
                'closed': 0,
                'merged': 0,
                'commented': 0,
                'reopened': 0,
                'opened': 0 }
    user_actions[user][action] += 1


def pp_user_actions():
    print "User                  |Opened|Closed|Merged|Commented|"
    for user in sorted(user_actions.keys()):
        print "{:<22}|{:>6}|{:>6}|{:>6}|{:>9}|".format(
                user,
                user_actions[user]['opened'],
                user_actions[user]['closed'],
                user_actions[user]['merged'],
                user_actions[user]['commented'])

if __name__ == "__main__":

    g = Github(config.token)
    pc = g.get_organization('puppet-community')

    user_actions = {}
    total_issues_created = 0
    total_issues_closed = 0
    total_merges = 0
    for repo in pc.get_repos():
        for issue in repo.get_issues(state='all'):

            # Handle creation
            if before(issue.created_at):
                user_action(issue.user.login, 'opened')
                total_issues_created += 1

            # Handle closure
            if issue.state == 'closed':
                if before(issue.closed_at):
                    user_action(issue.closed_by.login, 'closed')
                    total_issues_closed += 1

            # Handle merge
            if issue.state == 'closed' and before(issue.closed_at):
                if issue.pull_request is not None:
                    newrepo = g.get_repo('puppet-community/'+repo.name)
                    pr = newrepo.get_pull(issue.number)
                    if pr.merged:
                        if before(pr.merged_at):
                            user_action(pr.merged_by.login, 'merged')
                            total_merges += 1

            # Handle comments
            for comment in issue.get_comments():
                if before(comment.created_at):
                    user_action(comment.user.login, 'commented')


    print "Total Issues Created(last 30 days): {0}".format(total_issues_created)
    print "Total Issues Closed(last 30 days): {0}".format(total_issues_closed)
    print "Total PR Merges(last 30 days): {0}".format(total_issues_closed)
    print "Breakdown of last 30 days by user:"
    pp_user_actions()





