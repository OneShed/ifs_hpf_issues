#!/bin/env python3

# Create an issue overview of IFS applications.

import sys
import os
import json
from jsonmerge import merge

username='ifsadm'
passwd=''

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
        'AID026_Vestima_IFRD_UNIX',
        'AID026_Vestima_VESTIMA_PLUS_UNIX',
        'AID201_CDOC_CDOC_UNIX',
        'AID202_CCS_CCS_UNIX',
        'AID202_CCS_CCS_CORE_NT',
        'AID201_CDOC_CDOC_UNIX',
        'AID201_CDOC_CDOC_EXT_NT',
        'AID198_CORONA_CORONA_NT',
        'AID035_HUB_HUB_IREPORT_UNIX',
        'AID202_CCS_JCCS_UNIX',
        )

result=dict()
for p in projects:
	json_proj = api.get_findings(p)
	result=merge(result, json_proj)
	
json_pretty = json.dumps(result, indent=4, sort_keys=False)
write_file(json_pretty)
