#!/usr/bin/env python

from copy import deepcopy
from glob import glob
import os
import shutil
import yaml

base_path = os.path.join(os.path.dirname(__file__), "..")
generated_path = os.path.join(base_path, "generated")


# Helper method to allow for `literal` YAML syntax
def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:  # check for multiline string
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


yaml.add_representer(str, str_presenter)

os.mkdir(generated_path)

# Grafana
# Copy files
grafana_dashboard_path = os.path.join(base_path, "..", "grafana", "dashboards")
grafana_template_path = os.path.join(base_path, "templates", "grafana")
grafana_output_path = os.path.join(generated_path, "grafana")

print("Grafana")
print("=======")
print("Copying templates to output path")
print(f"{grafana_template_path} => {grafana_output_path}")
shutil.copytree(grafana_template_path, grafana_output_path)

# Load k8s dashboard template
dashboard_template_path = os.path.join(grafana_output_path, "dashboard.yaml")
with open(dashboard_template_path, "r") as template_file:
    k8s_template = yaml.safe_load(template_file)

    # Iterate over all dashboards
    dashboards = glob(os.path.join(grafana_dashboard_path, "*.json"))
    for json_dashboard in dashboards:
        # Copy the template and update with the appropriate values
        k8s_dashboard = deepcopy(k8s_template)
        k8s_dashboard["metadata"]["name"] = os.path.splitext(os.path.basename(json_dashboard))[0]
        k8s_dashboard["spec"]["name"] = os.path.basename(json_dashboard)
        k8s_dashboard["spec"]["url"] = f"https://raw.githubusercontent.com/datastax/dse-metric-reporter-dashboards/master/grafana/dashboards/{os.path.basename(json_dashboard)}"

        # Read in JSON dashboard
        with open(json_dashboard, "r") as json_file:
            k8s_dashboard["spec"]["json"] = json_file.read()

        # Write out the k8s dashboard file
        dashboard_filename = f"{k8s_dashboard['metadata']['name']}.dashboard.yaml"
        dashboard_output_path = os.path.join(generated_path, "grafana", dashboard_filename)

        print(f"Templating {json_dashboard} => {dashboard_output_path}")

        with open(dashboard_output_path, "w") as k8s_file:
            k8s_file.write(yaml.dump(k8s_dashboard))

# Delete original template from distribution
print("Removing template from generated directory")
print(dashboard_template_path)
os.remove(os.path.join(grafana_output_path, "dashboard.yaml"))
print("")

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
prometheus_output_path = os.path.join(generated_path, "prometheus")
prometheus_template_path = os.path.join(base_path, "templates", "prometheus")
service_monitor_path = os.path.join(prometheus_output_path, "service_monitor.yaml")
prometheus_config_path = os.path.join(base_path, "..", "prometheus", "prometheus.yml")

print("Prometheus")
print("=======")
print("Copying templates to output path")
print(f"{prometheus_template_path} => {prometheus_output_path}")
shutil.copytree(prometheus_template_path, prometheus_output_path)

# Load k8s service monitor template
with open(service_monitor_path, "r") as template_file:
    k8s_service_monitor = yaml.safe_load(template_file)

    # Load prometheus configuration file
    with open(prometheus_config_path, "r") as prometheus_file:
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
    with open(service_monitor_path, "w") as service_monitor_file:
        print("Writing out service monitor configuration")
        print(service_monitor_path)
        yaml.dump(k8s_service_monitor, service_monitor_file)
