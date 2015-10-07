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
collectd-python plugin to read both the number of nf_conntrack connections as well
as the maximum number permitted.

Michael Fincham <michael.fincham@catalyst.net.nz>
"""

import collectd

NF_CONNTRACK_MAX = "/proc/sys/net/netfilter/nf_conntrack_max"
NF_CONNTRACK_COUNT = "/proc/sys/net/netfilter/nf_conntrack_count"

PLUGIN="catalyst_conntrack"

def read_file_integer(path):
    """Read an integer from a file"""
    with open(path) as fp:
        return int(fp.read())

def collectd_configure(configuration):
    pass

def collectd_init():
    pass

def collectd_dispatch(value, value_type, type_instance):
    """
    Take the given value and dispatch it to collectd.
    Creates a value named like "PLUGIN.value_type-type_instance",
    e.g. "catalyst_conntrack.conntrack-current"
    """

    val = collectd.Values(plugin=PLUGIN)
    val.type = value_type
    val.type_instance = type_instance
    val.values = [value]
    val.dispatch()

def collectd_read():
    try:
        collectd_dispatch(read_file_integer(NF_CONNTRACK_COUNT), 'conntrack', 'current')
    except:
        collectd.warning("could not read nf_conntrack_max from %s" % NF_CONNTRACK_MAX)

    try:
        collectd_dispatch(read_file_integer(NF_CONNTRACK_MAX), 'conntrack', 'limit')
    except:
        collectd.warning("could not read nf_conntrack_count from %s" % NF_CONNTRACK_COUNT)

collectd.register_config(collectd_configure)
collectd.register_init(collectd_init)
collectd.register_read(collectd_read)
