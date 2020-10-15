#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, IBM
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


# Guide:
# https://docs.ansible.com/ansible/devel/dev_guide/developing_modules_documenting.html
# TODO: Test documentation,
# https://docs.ansible.com/ansible/latest/dev_guide/testing_documentation.html#testing-module-documentation
DOCUMENTATION = r''' ---
module: powervs
short_description: IBM Power Systems Virtual Servers Dynamic Inventory
description:
    - U(https://www.ibm.com/cloud/power-virtual-server)
    - How to generate an API Key
version_added: "2.9"
author: "Jay Carman (@jaywcarman)"
options:
    ibmcloud_api_key:
        description:
            - The IBM Cloud API key to authenticate with the IBM Cloud
              platform. This can also be provided via the environment
              variable 'IC_API_KEY'.
        type: str
        required: True
    pi_cloud_instance_id:
        description:
            - (Required for new resource) This is the Power Instance id
              that is assigned to the account
        required: True
        type: str
requirements:
    - ibm_cloud_sdk_core
'''

# TODO: Add examples
EXAMPLES = r'''
'''

# TODO: Document return data
RETURN = r''' # '''

from ansible.plugins.inventory import BaseInventoryPlugin
import ibm_cloud_sdk_core

class InventoryModule(BaseInventoryPlugin):

    NAME = 'ibm.cloudcollection.powervs'

    def verify_file(self, path):
        ''' return true/false if this is possibly a valid file for this
        plugin to consume '''
        valid = False
        if super(InventoryModule, self).verify_file(path):
            # base class verifies that file exists and is readable by
            # current user
            if path.endswith(
                    ('ibm_powervs.yaml', 'ibm_powervs.yml',
                     'powervs.yaml', 'powervs.yml')):
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache=True):

        super(InventoryModule, self).parse(inventory, loader, path, cache)

        config = self._read_config_data(path)

        ibmcloud_iam = ibm_cloud_sdk_core.IAMTokenManager(
            apikey=self.get_option('ibmcloud_api_key'))

        pcloud_id = self.get_option('pi_cloud_instance_id'))

        mydata = ibmcloud_powervs(token, pcloud_id)

        #parse data and create inventory objects:
        for colo in mydata:
            for server in mydata[colo]['servers']:
                self.inventory.add_host(server['name'])
                self.inventory.set_variable(server['name'], 'ansible_host', server['external_ip'])
