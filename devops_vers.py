#!/bin/env python3

# Just print the IFS DevOps ProjectVersions 

import sys
import os
import json

username='ifsadm'
passwd='hes5!wucRusece'

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
        if 'SCHEDULED' in v or 'DEVELLPER' in v or 'PRE_RELEASE' in v:
            print(v)
