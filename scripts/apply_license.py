#!/usr/bin/env python
import argparse
import base64
import json
import urllib2
import ssl

LICENSE = {
    "subscription_name": "Enterprise Tower up to 30 Nodes",
    "features": {},
    "instance_count": 30,
    "trial": False,
    "eula_accepted": True,
    "contact_email": "demos@ansible.com",
    "company_name": "Ansible, Inc.",
    "license_type": "enterprise",
    "contact_name": "Demo User",
    "license_date": 1735707600,
    "license_key": "367ce98cba3e62f4c5665c567f6018ec74fdb35530247d6e0bcbe753cbb8fa88"
}

parser = argparse.ArgumentParser()
parser.add_argument(
    '-u',
    '--username',
    dest='username',
    required=True,
    help='Admin username'
)
parser.add_argument(
    '-p',
    '--password',
    dest='password',
    required=True,
    help='Admin password'
)
parser.add_argument('base_url', help='Base url')


def run():
    args = parser.parse_args()

    # create https handler
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    https_handler = urllib2.HTTPSHandler(context=ctx)

    # create url opener
    opener = urllib2.build_opener(https_handler)
    urllib2.install_opener(opener)

    # encode credentials
    encoded_credentials = base64.b64encode('%s:%s' % (args.username, args.password))

    # make POST request to add the license
    headers = {
        'Authorization': 'Basic %s' % encoded_credentials,
        'Content-type': 'application/json'
    }
    request = urllib2.Request(
        args.base_url + '/api/v2/config/',
        json.dumps(LICENSE),
        headers
    )

    urllib2.urlopen(request)


if __name__ == '__main__':
    run()
