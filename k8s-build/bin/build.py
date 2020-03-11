#!/usr/bin/env python

from copy import deepcopy
from glob import glob
import os
import shutil
import yaml

output_path = "generated"


# Helper method to allow for `literal` YAML syntax
def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:    # check for multiline string
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


yaml.add_representer(str, str_presenter)

os.mkdir(output_path)

# Grafana
# Copy files
shutil.copytree(os.path.join("templates", "grafana"), os.path.join(output_path, "grafana"))

# Load k8s dashboard template
with open(os.path.join(output_path, "grafana", "dashboard.yaml"), "r") as template_file:
    k8s_template = yaml.safe_load(template_file)

    # Iterate over all dashboards
    dashboards = glob(os.path.join("..", "grafana", "dashboards", "*.json"))
    for json_dashboard in dashboards:
        # Copy the template and update with the appropriate values
        k8s_dashboard = deepcopy(k8s_template)
        k8s_dashboard["metadata"]["name"] = os.path.splitext(os.path.basename(json_dashboard))[0]
        k8s_dashboard["spec"]["name"] = os.path.basename(json_dashboard)

        # Read in JSON dashboard
        with open(json_dashboard, "r") as json_file:
            k8s_dashboard["spec"]["json"] = json_file.read()

        # Write out the k8s dashboard file
        dashboard_path = os.path.join(output_path, "grafana", f"{k8s_dashboard['metadata']['name']}.dashboard.yaml")
        with open(dashboard_path, "w") as k8s_file:
            k8s_file.write(yaml.dump(k8s_dashboard))

# Delete original template from distribution
os.remove(os.path.join(output_path, "grafana", "dashboard.yaml"))


# Prometheus
key_mapping = {
    'action': 'action',
    'regex': 'regex',
    'replacement': 'replacement',
    'separator': 'separator',
    'source_labels': 'sourceLabels',
    'target_label': 'targetLabel'
}

# Copy files
shutil.copytree(os.path.join("templates", "prometheus"), os.path.join(output_path, "prometheus"))

# Load k8s service monitor template
with open(os.path.join(output_path, "prometheus", "service_monitor.yaml"), "r") as template_file:
    k8s_service_monitor = yaml.safe_load(template_file)

    # Load prometheus configuration file
    with open(os.path.join("..", "prometheus", "prometheus.yml"), "r") as prometheus_file:
        prometheus_conf = yaml.safe_load(prometheus_file)

        # Extract scrape configs
        for scrape_config in prometheus_conf['scrape_configs']:
            if scrape_config['job_name'] == "dse":
                # Extract relabel configs
                for relabel_config in scrape_config['metric_relabel_configs']:
                    k8s_relabel_config = {}

                    # Rename keys and move to template
                    for pair in relabel_config.items():
                        if pair[0] in key_mapping:
                            k8s_relabel_config[key_mapping[pair[0]]] = pair[1]
                        else:
                            print(f"Missing mapping for {pair[0]}")

                    k8s_service_monitor['spec']['endpoints'][0]['metricRelabelings'].append(k8s_relabel_config)

        # Write out templated k8s service monitor
    with open(os.path.join(output_path, "prometheus", "service_monitor.yaml"), "w") as service_monitor_file:
        yaml.dump(k8s_service_monitor, service_monitor_file)
