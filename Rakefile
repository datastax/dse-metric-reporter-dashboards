require 'yaml'

task :set_version, [:new_version] do |t, args|
    File.open("VERSION.txt", "w") do |f|
        f.write(args.new_version)
    end
end

task :clean do |t|
    FileUtils.rm_r "dist"
end

task build: [:clean] do |t|
    FileUtils.mkdir "dist"

    # Grafana
    ## Copy files
    FileUtils.cp_r "grafana", "dist"

    ## Load k8s dashboard template
    k8s_template_path = File.join "dist", "grafana", "k8s", "dashboard.yaml"
    k8s_template = YAML::load_file k8s_template_path

    ## Iterate over all defined dashboards
    json_dashboard_path_glob = File.join "dist", "grafana", "dashboards", "*.json"
    Dir.glob(json_dashboard_path_glob).each do |json_dashboard|
        ## Copy the template and update with the appropriate values
        k8s_dashboard = Marshal.load(Marshal.dump(k8s_template))
        k8s_dashboard["metadata"]["name"] = File.basename(json_dashboard, ".json")
        k8s_dashboard["spec"]["name"] = File.basename(json_dashboard)

        File.open(json_dashboard, "r") do |f|
            k8s_dashboard["spec"]["json"] = f.read
        end

        ## Write out the k8s dashboard file
        File.open(File.join("dist", "grafana", "k8s", "#{k8s_dashboard["metadata"]["name"]}.dashboard.yaml"), "w") do |f|
            f.puts YAML::dump(k8s_dashboard)
        end
    end

    ## Delete original template from distribution
    File.delete k8s_template_path


    # Prometheus
    key_mapping = {
        "action" => "action",
        "regex" => "regex",
        "replacement" => "replacement",
        "separator" => "separator",
        "source_labels" => "sourceLabels",
        "target_label" => "targetLabel"
    }

    ## Copy files
    FileUtils.cp_r "prometheus", "dist"

    ## Load k8s service monitor template
    k8s_template_path = File.join "dist", "prometheus", "k8s", "service_monitor.yaml"
    k8s_service_monitor = YAML::load_file k8s_template_path

    ## Load prometheus configuration
    prometheus_conf = YAML::load_file File.join("dist", "prometheus", "prometheus.yml")
    prometheus_conf["scrape_configs"].each do |scrape_config|
        if scrape_config["job_name"] == "dse"
            scrape_config["metric_relabel_configs"].each do |relabel_config|
                k8s_relabel_config = {}

                relabel_config.each_pair do |k, v|
                    if key_mapping.key? k
                    k8s_relabel_config[key_mapping[k]] = relabel_config[k]
                    else
                        puts "Missing mapping for #{k}"
                    end
                end

                k8s_service_monitor["spec"]["endpoints"][0]["metricRelabelings"] << k8s_relabel_config
            end
        end
    end

    ## Write out templated k8s service monitor
    File.open File.join("dist", "prometheus", "k8s", "service_monitor.yaml"), "w" do |f|
        f.puts YAML::dump(k8s_service_monitor, options = {line_width: -1})
    end
end

task package: [:build] do |t|
    File.open "VERSION.txt" do |f|
        version = f.read
        
        Dir.chdir "dist"
        exec "zip -r -9 dse-metrics-reporter-dashboards-#{version}.zip ."
    end
end
