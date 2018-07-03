#!/bin/env python3

# Print out all jenkins jobs

import sys
import os
import jenkins
import json

username='ifsadm'
jenkins_url='http://vmcdelifsdev:8800'

def get_passwd(user):

    if user==None:
        raise(Exception("User not specified"))

    hostname = None
    if 'HOSTNAME' in os.environ:
        hostname = os.environ['HOSTNAME']

    else:
        command = 'hostname -s'
        p = subprocess.Popen(command.split(), stdout=subprocess.PIPE, shell=True)
        std_out, std_err = p.communicate()
        if p.returncode != 0:
            if hostname == None:
                raise (Exception("Cannot retrieve hostname"))
        else:
            hostname = std_out.split('.')[0]

    command = "/bin/get_passwd %s %s" % (user, hostname)

    p = subprocess.Popen(command.split(), stdout=subprocess.PIPE, shell=False)
    std_out, std_err = p.communicate()
    if p.returncode != 0:
        raise (Exception("Cannot retrieve password"))

    return std_out.strip()

passwd=get_passwd(username)

def json_pprint(self, dict=dict):
    jsond = json.dumps(dict, indent=4, sort_keys=False)
    print( jsond )

# TODO
def browse_folder(folder):
    pass

server = jenkins.Jenkins(jenkins_url, username=username, password=passwd)
jobs = server.get_jobs()

folders=list()
for j in jobs:
    folders.append(j['url'])

folders2=list()
for fol in folders:
    try:
        jb=jenkins.Jenkins(fol, username=username, password=passwd)
        jobs2 = jb.get_jobs()
    except KeyError:
        continue
    for k in jobs2:
        folders2.append(k['url'])

vers=list()
for fol in folders2:
    try:
        jb2=jenkins.Jenkins(fol, username=username, password=passwd)
        jobs3 = jb2.get_jobs()
    except KeyError:
        continue
    for k in jobs3:
        ur=k['url']
        ur=ur[:-1]

        ur=ur.rsplit('/',1)[-1]
        vers.append(ur)

versions='\n'.join(vers)
f = open('/tmp/jenkins_jobs', 'w')
f.write(versions)

