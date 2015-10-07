#!/usr/bin/env python
#
# Copyright (c) 2015 Catalyst.net Ltd
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
collectd-python plugin to read nfacct metrics. Presently executes the `nfacct' utility, which could be improved upon.

Michael Fincham <michael.fincham@catalyst.net.nz>
"""

import collectd
import subprocess

NFACCT = "/usr/sbin/nfacct"

PLUGIN = "netfilter_acct"
PREFIX = ""
INTERVAL = 10 # seconds

def retrieve_accounting():
    nfacct_output = subprocess.check_output([NFACCT, 'list'], shell=False).strip()

    for line in nfacct_output.splitlines(False):
        record = line.split()
        pkts = int(record[3].strip(','))
        bytes = int(record[6].strip(','))
        name = " ".join(record[9:]).strip(';')

        if name.startswith(PREFIX):
            name = name[len(PREFIX):]
            val = collectd.Values(plugin=PLUGIN)
            val.type = 'ipt_packets'
            val.plugin_instance = name
            val.values = [pkts]
            val.dispatch(interval=INTERVAL)

            val = collectd.Values(plugin=PLUGIN)
            val.plugin_instance = name
            val.type = 'ipt_bytes'
            val.values = [bytes]
            val.dispatch(interval=INTERVAL)


def collectd_configure(configuration):
    global PREFIX

    for node in configuration.children:
        if node.key.upper() == 'PREFIX':
            PREFIX = str(node.values[0])

def collectd_init():
    collectd.register_read(retrieve_accounting, interval=INTERVAL, name='python.%s' % retrieve_accounting.__module__)

collectd.register_config(collectd_configure)
collectd.register_init(collectd_init)