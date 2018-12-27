#!/bin/env python3

# Remove deleted versions from SSC 

import sys
import os
import json

import subprocess

username='ifsadm'
jenkins_jobs='/usr/local/share/tmp/jenkins_jobs'

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

hpfortify_api='/local/git/hpfortify_api'
datadir = os.path.join(hpfortify_api, 'data')
json_filename = '/tmp/ifs_hpf_issues.json'

jobs=open(jenkins_jobs, 'r')
jobs_str=jobs.readlines()

sys.path.append(hpfortify_api)
import hpfortify_api

api = hpfortify_api.Api(username=username, passwd=passwd, verify_ssl=False, datadir=datadir)

data=()
with open(json_filename) as f:
    data = json.load(f) 

def not_in_jobs(version):
    for j in jobs_str:
        jj = j.strip()

        if jj.find(version) != -1: 
            return False

    return True

for d in data:
    for v in data[d]:

        if v=='DEV':
            continue

        if v=='Release':
            continue

        if v=='QAE':
            continue

        if v=='ARTEFACT':
            continue

        if not_in_jobs(v): 
            api.delete_project_version(d, v)
