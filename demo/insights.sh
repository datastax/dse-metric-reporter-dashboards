#!/bin/bash

# Download the promethius configs

mkdir prometheus

curl https://raw.githubusercontent.com/datastax/dse-metric-reporter-dashboards/master/prometheus/prometheus.yml -o prometheus/prometheus.yml
# Download tg_dse.json preconfigured for insites tutorial
curl https://raw.githubusercontent.com/datastax/dse-metric-reporter-dashboards/master/demo/tg_dse.json -o prometheus/tg_dse.json

# Download the grafana configs

mkdir grafana
curl https://raw.githubusercontent.com/datastax/dse-metric-reporter-dashboards/master/grafana/dashboards.yaml -o grafana/dashboards.yaml
curl https://raw.githubusercontent.com/datastax/dse-metric-reporter-dashboards/master/grafana/prometheus-datasource.yaml -o grafana/prometheus-datasource.yaml

# Makd dashboards directory
mkdir grafana/dashboards

curl https://raw.githubusercontent.com/datastax/dse-metric-reporter-dashboards/master/grafana/dashboards/dse-cluster-condensed.json -o grafana/dashboards/dse-cluster-condensed.json
curl https://raw.githubusercontent.com/datastax/dse-metric-reporter-dashboards/master/grafana/dashboards/dse-cluster-metrics.json -o grafana/dashboards/dse-cluster-metrics.json
curl https://raw.githubusercontent.com/datastax/dse-metric-reporter-dashboards/master/grafana/dashboards/prometheus-metrics.json -o grafana/dashboards/prometheus-metrics.json
curl https://raw.githubusercontent.com/datastax/dse-metric-reporter-dashboards/master/grafana/dashboards/system-metrics.json -o grafana/dashboards/system-metrics.json

# Download promethius conf for dse 

curl https://raw.githubusercontent.com/datastax/dse-metric-reporter-dashboards/master/demo/prometheus.conf -o prometheus.conf

# Download Docker compose yaml
curl https://raw.githubusercontent.com/roberd13/insights-tutorial/master/demo/dse-and-prom-compose.yml -o dse-and-prom-compose.yml
