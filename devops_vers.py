#!/bin/env python3

# Just print the IFS DevOps ProjectVersions 

import sys
import os
import json

username='ifsadm'

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
json_filename = '/usr/local/share/ifs_hpf_issues/ifs_hpf_issues.json'
datadir = os.path.join(hpfortify_api, 'data')

sys.path.append(hpfortify_api)
import hpfortify_api

api = hpfortify_api.Api(username=username, passwd=passwd, verify_ssl=False, datadir=datadir)

def write_file(json_proj):
	issues_file = open(json_filename, 'w')
	issues_file.write(json_proj)
	issues_file.close()

projects=(
        'AID026_Vestima_VESTIMA_PLUS_UNIX',
        'AID026_Vestima_IFRD_UNIX',
        'AID026_Vestima_OXYGEN_UNIX',
        'AID455_Oxygen_OXYGEN_UNIX',
        'AID201_CDOC_CDOC_UNIX',
        'AID202_CCS_CCS_UNIX',
        'AID202_CCS_CCS_CORE_NT',
        'AID201_CDOC_CDOC_UNIX',
        'AID201_CDOC_CDOC_EXT_NT',
        'AID198_CORONA_CORONA_NT',
        'AID035_HUB_HUB_IREPORT_UNIX',
        'AID202_CCS_JCCS_UNIX',
        )

for p in projects:
    for v in api.get_project_versions(p, sort=True):
        if 'SCHEDULED' in v or 'DEVELOPER' in v or 'PRE_RELEASE' in v:
            print(v)
