# Kubernetes Custom Resources

These dashboards and prometheus configuration files may be transformed via the collection of Python scripts under `bin/`.

Specifically run `bin/clean.py && bin/build.py` to generate appropriate files in the `k8s-build/generated` directory. These files integrate with the Custom Resources defined by the [Prometheus](https://operatorhub.io/operator/prometheus) and [Grafana](https://operatorhub.io/operator/grafana-operator) operators available on Operator Hub.


### Prometheus
The [Prometheus Operator](https://operatorhub.io/operator/prometheus) handles the orchestration, configuration, and deployment of k8s resources required for a HA Prometheus installation. Rather than specifying a list of DSE nodes in a JSON file we direct Prometheus to monitor a Kubernetes [Service](https://kubernetes.io/docs/concepts/services-networking/service/) which exposes all DSE nodes via DNS. This mapping of hosts is handled by a `ServiceMonitor` Custom Resource defined by the operator. The following steps illustrate how to install the Prometheus operator, deploy a service monitor pointed at a DSE cluster (with metric relabeling), and  deploy a HA prometheus cluster connected to the service monitor.

1. Install the OperatorHub Lifecycle Manager (OLM)
   
   `curl -sL https://github.com/operator-framework/operator-lifecycle-manager/releases/download/0.15.1/install.sh | bash -s 0.15.1`
   
   This installs a number of custom resource definitions and an operator that handles installing _other_ operators.

1. Install the Prometheus Operator
   
   `kubectl create -n cass-operator -f k8s-build/generated/prometheus/operator.yaml`

   This will pull down and start the Prometheus operator along with a configuration indicating it should watch the `default` namespace for resources it manages. Should the installation require different namespaces change the values within this file and re-apply it to the cluster.

1. Configure and install the Service Monitor
   
   Before installation edit the service monitor's YAML to include the appropriate labels that match your cluster's service. For example if your cluster service has the label `cassandra.datastax.com/cluster: cluster-name` this mapping would be included in the service monitor yaml under `spec.selector.matchLabels`. As a convenience we have included the example here in the generated `service_monitor.yaml`.

   _Note: To check the labels on your service run the following command_

   `kubectl get svc -n cass-operator --show-labels=true`
   
   With the configuration file updated apply the resource to the cluster.
   
   `kubectl apply -n cass-operator -f k8s-build/generated/prometheus/service_monitor.yaml`

1. Configure and install the Prometheus deployment
   
   Similar to the service and service monitor mapping, the instance must be provided with a set of labels to match service monitors to Prometheus deployments. The following section in the `Prometheus` custom resource maps the deployment to all service monitors with the label `cassandra.datastax.com/cluster: cluster-name`
  
   ```
     serviceMonitorSelector:
       matchLabels:
         cassandra.datastax.com/cluster: cluster-name
   ```
   
   After adjustments apply this file to the cluster

   `kubectl apply -n cass-operator -f k8s-build/generated/prometheus/instance.yaml`


### Grafana
The [Grafana Operator](https://operatorhub.io/operator/grafana-operator) handles the orchestration, configuration, and deployment of k8s resources required for a Grafana installation. Instead of configuring datasources, dashboards, and deployments via the GUI everything is configured via YAML files in this repo. The following steps illustrate how to install the Grafana operator, data source pointed at the previously deployed prometheus, a collection of dashboards, and an instance of the grafana application.

1. Install the OperatorHub Lifecycle Manager (OLM) if you haven't already
   
   `curl -sL https://github.com/operator-framework/operator-lifecycle-manager/releases/download/0.15.1/install.sh | bash -s 0.15.1`
   
   This installs a number of custom resource definitions and an operator that handles installing _other_ operators.

1. Install the Grafana Operator
   
   `kubectl create -n cass-operator -f k8s-build/generated/grafana/operator.yaml`

   This will pull down and start the Grafana operator along with a configuration indicating it should watch the `default` namespace for resources it manages. Should the installation require different namespaces change the values within this file and re-apply it to the cluster.

1. Configure and install the `GrafanaDataSource`
   
   Before installation edit the YAML to point at the instantiated prometheus cluster. If you are not sure what value to use check the output of `kubectl get svc` for the prometheus service name.
   
   With the configuration file updated apply the resource to the cluster.
   
   `kubectl apply -n cass-operator -f k8s-build/generated/grafana/datasource.yaml`

1. Configure and install the `GrafanaDashboard`
   
   Before installation edit the YAML with appropriate labels. In this example a label of `app=grafana` is used. With the configuration file updated apply the resource to the cluster.
   
   `kubectl apply -n cass-operator -f k8s-build/generated/grafana/`

1. Configure and install the Grafana deployment
   
   The deployment must be informed of labels to check for matching dashboards. The following section in the `Grafana` custom resource maps the deployment to all dashboards with the label `app=grafana`
  
   ```
     dashboardLabelSelector:
       - matchExpressions:
           - key: app
             operator: In
             values:
               - grafana
   ```
   
   After adjustments apply this file to the cluster

   `kubectl apply -n cass-operator -f k8s-build/generated/grafana/instance.yaml`

1. Port forward to the grafana instance and check it out at http://127.0.0.1:3000/ (username: admin, password: secret)
   
   `kubectl port-forward -n cass-operator svc/grafana-service 3000`
