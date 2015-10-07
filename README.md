# collectd-network

collectd-python plugins useful for monitoring networking things in linux.

## catalyst_interface.py

Compatible with the standard `interface' plugin but extends the schema of /etc/network/interfaces to include a description property.

<pre>
&lt;LoadPlugin python&gt;
    Globals true
&lt;/LoadPlugin&gt;

&lt;Plugin python&gt;
    ModulePath &quot;/path/where/module/installed&quot;
    LogTraces true
    Interactive false
    Import &quot;catalyst_interface&quot;

    &lt;Module catalyst_interface&gt;
    &lt;/Module&gt;
&lt;/Plugin&gt;

# if you need to keep the standard interface plugin loaded, something like this
# will at least stop it from also reporting.
&lt;Plugin &quot;interface&quot;&gt;
  Interface &quot;not-an-interface&quot;
  IgnoreSelected false
&lt;/Plugin&gt;
</pre>

## catalyst_conntrack

Read both the number of nf_conntrack connections as well as the maximum number permitted. Will report unhelpful figures if nf_conntrack_tcp_loose is enabled (which it is by default).

<pre>
&lt;LoadPlugin python&gt;
    Globals true
&lt;/LoadPlugin&gt;

&lt;Plugin python&gt;
    ModulePath &quot;/path/where/module/installed&quot;
    LogTraces true
    Interactive false
    Import &quot;catalyst_conntrack&quot;

    &lt;Module catalyst_conntrack&gt;
    &lt;/Module&gt;
&lt;/Plugin&gt;
</pre>

## netfilter_acct

Read nfacct metrics. Presently executes the `nfacct' utility, which could be improved upon.

<pre>
&lt;LoadPlugin python&gt;
    Globals true
&lt;/LoadPlugin&gt;

&lt;Plugin python&gt;
    ModulePath &quot;/path/where/module/installed&quot;
    LogTraces true
    Interactive false
    Import &quot;netfilter_acct&quot;

    &lt;Module netfilter_acct&gt;
    &lt;/Module&gt;
&lt;/Plugin&gt;
</pre>
