#!/usr/bin/env python

import json
from github import Github
from datetime import datetime, timedelta
import config

from collections import defaultdict

def totimestamp(dt, epoch=datetime(1970,1,1)):
    td = dt - epoch
    # return td.total_seconds()
    return int((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1e6 )


if __name__ == "__main__":

    g = Github(config.token)
    pc = g.get_organization('puppet-community')

    user_actions = {}
    for repo in pc.get_repos():
        #from pdb import set_trace; set_trace()
        print repo.name
        for event in repo.get_issues_events():
            try:
                username = event.actor.login
            except:
                continue

            #from pdb import set_trace; set_trace()
            if event.created_at < (datetime.now() - timedelta(30)):
                continue

            print username, event.created_at, event.event
            if event.event in ['closed', 'merged', 'reopened', 'opened']:
                print username, "did", event.event
                if username not in user_actions.keys():
                    user_actions[username] = {
                            'closed': 0,
                            'merged': 0,
                            'reopened': 0,
                            'opened': 0 }
                else:
                    user_actions[username][event.event] += 1


    print user_actions





