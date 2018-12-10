# Metrics Collector Demo Using Docker Images

### In this simple Demo we will walk through enabling the new DSE Metrics Collector in a DataStax Enterprise (DSE) 6.7 Docker Container, exporting the metrics to a Prometheus Docker Container and visualizing these metrics with a Grafana Docker container.

This Demo is created using a DSE 6.7, Prometheus 2.4.3 and Grafana 5.3.2 containers.

## Prerequisites

* A computer running MacOSX, Linux or a Linux Virtual Machine

* Basic understanding of Docker images and containers. 

* Docker installed on your local system, see [Docker Installation Instructions](https://docs.docker.com/engine/installation/). 

* Docker Compose installed, if running linux see [Install Docker Compose](https://docs.docker.com/compose/install)

* DataStax DSE Docker Images are hosted on [Docker Hub](https://hub.docker.com/r/datastax/dse-server/). For documentation including configuration options, environment variables, and compose examples head over to our official [Docker Docs](https://docs.datastax.com/en/docker/doc/index.html?utm_campaign=Docker_Cus_2019&utm_medium=web&utm_source=docker&utm_term=&utm_content=Web_DocsDocker)

## Getting Started

Lets start by creating a directory to work from.  From a CLI prompt create a directory in your home directory called insights and change to that directory


```
mkdir ~/insights && cd ~/insights
```

## Demo Data

To get the demo data, we need to clone the [DataStax DSE Metrics Reporter GitHub](https://github.com/datastax/dse-metric-reporter-dashboards) reop with the following command

```
curl -Lo dse-metric-reporter-dashboards-master.zip https://github.com/datastax/dse-metric-reporter-dashboards/archive/master.zip && unzip dse-metric-reporter-dashboards-master.zip
```

Now we need to cd to the demo directory 

```
cd dse-metric-reporter-dashboards-master/demo
```

## Starting the Containers

Next start the containers with `docker-compose` using the downloaded insights-compose.yaml 

```
docker-compose -f dse-and-prom-compose.yml up -d 
```

The dse-and-prom-compose.yml 
* Pulls the images from Docker Hub
* Creates a bridged network for the containers to communicate on
* Maps the volumes to containers with the files we downloaded
* Publishes the ports for insights, prometheus and grafana
* Creates an alias for the dse container to use as the address in our custom `tg_dse.json` 

## Configuring DSE to send metrics

Now we need to configure the dse container to send metrics to prometheus. To do this we have a preconfigured prometheus.conf file you downloaded earlier.  We need to copy this to the DSE container.

```
docker cp prometheus.conf dse-server:/opt/dse/resources/dse/collectd/etc/collectd/prometheus.conf
```

Next we need to stop and restart metrics collecton

```
docker exec -it dse-server dsetool insights_config --mode DISABLED
```

```
docker exec -it dse-server dsetool insights_config --mode ENABLED_WITH_LOCAL_STORAGE
```

## Viewing the Metrics in Grafana

It may take a few minutes for metrics to populate but everything should be up and running and you can now see the metrics using the preconfigured grafana dashboards by visiting 

http://localhost:3000/dashboards or http://docker-host-ip:3000/dashboards if running on a remote host.

![DSE Cluster Condensed](https://github.com/datastax/dse-metric-reporter-dashboards/blob/master/doc/DSEMetricsCollectorDashboardCondensed.png)

## Destroy the Demo

Destroying the demo is as simple as running the command 

```
docker-compose -f  dse-and-prom-compose.yml down
```

All the config files are still located on your host so if you decided to run the demo again, as long as you do not delete the data in `~/insights` all you have to do is run the below command again from the `~/insights/dse-metric-reporter-dashboards/demo` directory and you will be back where you were prior to destroying.

```
docker-compose -f  dse-and-prom-compose.yml up -d 
```

## Whats Next

If you want more granular configuration details, using an existing promethius and grafana servers or instructions to configure metrics collector with existing clusters check out the offical DataStax [Metrics Collector Documentation](https://docs.datastax.com/en/dse/6.7/dse-dev/datastax_enterprise/tools/metricsCollector/mcIntroduction.html)
