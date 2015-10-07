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
collectd-python plugin compatible with the included `interface' plugin but which supplies
the description of the interface (from /etc/network/interfaces) along with the interface name.

Michael Fincham <michael.fincham@catalyst.net.nz>
"""

import collectd

PROC_NET_DEV = "/proc/net/dev"
ETC_NETWORK_INTERFACES = "/etc/network/interfaces"

PLUGIN = "interface"
INTERFACES = []
INVERT = False

def collectd_configure(configuration):
    global INTERFACES, INVERT

    for node in configuration.children:
        if node.key == 'Interface':
            INTERFACES.append(node.values[0])
        elif node.key == 'IgnoreSelected':
            INVERT = bool(node.values[0])

def collectd_init():
    pass

def collectd_dispatch(plugin_instance, values, value_type):
    """
    Take the given value and dispatch it to collectd.
    Creates a value named like "PLUGIN.value_type-type_instance",
    e.g. "catalyst_conntrack.conntrack-current"
    """

    val = collectd.Values(plugin=PLUGIN)
    val.plugin_instance = plugin_instance
    val.type = value_type
    val.values = values
    val.dispatch()

def collectd_read():
    """
    Read the values from /proc/net/dev and dispatch them to collectd.
    """

    descriptions = {}

    # simple crummy parser for /etc/network/interfaces, doesn't try too hard
    current_interface = ''
    try:
        with open(ETC_NETWORK_INTERFACES) as fp:
            for line in fp:
                line = line.strip()

                try:
                    if line.startswith('iface'):
                        current_interface = line.split()[1]
                    elif line.startswith('description'):
                        descriptions[current_interface] = " ".join(line.split()[1:])
                except:
                    continue
    except:
        pass # if there's no interfaces file, oh well.

    with open(PROC_NET_DEV) as fp:
        for line in fp:
            if ":" not in line: # no ':' means it's not an interface
                continue

            rx = {}
            tx = {}

            (ifname, rx['bytes'], rx['packets'], rx['errs'], rx['drop'],
            rx['fifo'], rx['frame'], rx['compressed'], rx['multicast'],
            tx['bytes'], tx['packets'], tx['errs'], tx['drop'], tx['fifo'],
            tx['colls'], tx['carrier'], tx['compressed']) = line.strip().split()

            ifname = ifname[:-1] # remove the trailing colon

            if len(INTERFACES) == 0 or (ifname in INTERFACES and not INVERT) or (ifname not in INTERFACES and INVERT):
                if ifname in descriptions:
                    ifname = "%s %s" % (ifname, descriptions[ifname])

                collectd_dispatch(ifname, (rx['bytes'], tx['bytes']), 'if_octets')
                collectd_dispatch(ifname, (rx['packets'], tx['packets']), 'if_packets')
                collectd_dispatch(ifname, (rx['drop'], tx['drop']), 'if_errors')

collectd.register_config(collectd_configure)
collectd.register_init(collectd_init)
collectd.register_read(collectd_read)
