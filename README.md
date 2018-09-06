# dse-metric-reporter-dashboards

Some basics on getting things up and running

## Install

clone this repo and then you'll need to install:

* docker
* docker-compose

Follow the links below to install the docker tools:

https://docs.docker.com/install/linux/docker-ce/ubuntu/

https://docs.docker.com/compose/install/

Once you have those installed and working and you have cloned this repo,
cd to where you cloned this repo and run

```
docker-compose up
```

Then connect to the dashboard on port 3000 in your browser.

## Setup

Once you have the dashboard setup you'll then need to add your cluster into it. This example is based on Ubuntu 14.04 and assumes you already have installed a DSE6.7 cluster and its up and running.

### DSE nodes

By default the DSE6.7 nodes will have collectd configured, check this is running by running the following command

```
$ dsetool insights_config --show_config
{
  "mode" : "ENABLED_WITH_LOCAL_STORAGE",
  "config_refresh_interval_in_seconds" : 30,
  "metric_sampling_interval_in_seconds" : 30,
  "data_dir_max_size_in_mb" : 1024,
  "node_system_info_report_period" : "PT1H"
}
```

Now you'll need to comment in the lines in the following file, using a ctool command:

```
ctool run my_cluster all 'sudo sed -i "s/^#//g" /usr/share/dse/collectd/etc/collectd/10-write-prom.conf'
```

To check

```
ctool run general all 'sudo cat /usr/share/dse/collectd/etc/collectd/10-write-prom.conf'
```

Example file:

```
$ cat /usr/share/dse/collectd/etc/collectd/10-write-prom.conf

LoadPlugin write_prometheus

<Plugin write_prometheus>
  Port "9103"
</Plugin>
```

You will need to restart DSE to get this running, check the node is listening on port 9103 (as well as the usual ports)

```
$ netstat -lnt
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 10.200.181.237:8081     0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:9042            0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN
tcp        0      0 10.200.181.237:7000     0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:7199            0.0.0.0:*               LISTEN
tcp        0      0 10.200.181.237:8609     0.0.0.0:*               LISTEN
tcp        0      0 10.200.181.237:8778     0.0.0.0:*               LISTEN
tcp6       0      0 :::9103                 :::*                    LISTEN
tcp6       0      0 :::22                   :::*                    LISTEN
```

### Dashboard containers

Now you'll need to add your cluster nodes into the dashboard containers

Find the `prometheus/tg_dse.json` file.
Add your nodes into a file like so:

**note the `cluster` needs to match your cluster name**

```
# cat prometheus/tg_dse.json
[
  {
    "targets": [
      "10.200.181.237:9103",
      "10.200.181.240:9103",
      "10.200.181.246:9103"
    ],
    "labels": {
      "cluster": "general"
    }
  }
]
```

Then restart the containers (you can use `docker restart <container>` on both containers, or user `docker stop <container>` on both containers and then `docker compose up` to restart both.

### Checking

Once you have everything running again go to your dashboard and then check you see information on your nodes.

Here are some things you can check to help troubleshooting:

`http://<dashboard_ip>:9090/targets` - this should show each of your DSE node as a target

`http://<dashboard ip>:3000/datasources/edit/1` - this should show the local prometheus container as a data source
  
  
