#!/usr/bin/env python

from xmlrpc.client import ServerProxy

REMOTE = ServerProxy('https://www-bd.fnal.gov/xmlrpc/Remote')

blah = REMOTE.Remote.drf('0:289124.SETTING', 42)

print(blah)
