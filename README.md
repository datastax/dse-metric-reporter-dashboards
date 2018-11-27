# DSE Metrics Collector Dashboards

This repository contains preconfigured Grafana dashboards that integrate with DSE Metrics Collector. Use DSE Metrics Collector to export DSE metrics to a monitoring tool like Prometheus, and then visualize DSE metrics in the Grafana dashboards.

Use Docker and modify the provided Prometheus configuration file, or manually export DSE metrics to an existing Prometheus server. Although the examples in the linked documentation use Promtheus as the monitoring tool, you can export the aggregated metrics to other tools like Graphite and Splunk.

## Getting started

Clone this repository and then follow the instructions in the DataStax documentation based on your implementation:

* [Export and visualize metrics with Prometheus and Docker](https://docs.datastax.com/en/dse/6.7/dse-dev/datastax_enterprise/tools/metricsCollector/mcExportMetricsDocker.html)
* [Manually export and visualize metrics with Prometheus](https://docs.datastax.com/en/dse/6.7/dse-dev/datastax_enterprise/tools/metricsCollector/mcExportMetricsManually.html)

## Examples

The following screenshots illustrate the preconfigured dashboards in this repository.

#### DSE Cluster Condensed
![DSE Cluster Condensed](DSEMetricsCollectorDashboardCondensed.png)

#### DSE System & Node Metrics
![DSE System and Node Metrics](DSEMetricsCollectorDashboardSystems.png)

#### DSE Cluster Latest
![DSE Cluster Latest](DSEMetricsCollectorDashboardLatest.png)

#### Promtheus Statistics
![Promtheus Statistics](DSEMetricsCollectorDashboardPrometheus.png)
