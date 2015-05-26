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

    members = 0
    # embarassing that we can't ask this
    for i in pc.get_members():
        members += 1

    print "Community Members: %s" % members
    print "Repos: %s" % pc.public_repos
