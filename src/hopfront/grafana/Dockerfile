# Authentication problems with 10.2 Lock to 10.1.5 for now.
FROM grafana/grafana:10.1.5
ADD grafana.ini /etc/grafana/grafana.ini
ADD prometheus.yaml /etc/grafana/provisioning/datasources/prometheus.yaml
ADD hopittydashboards.yaml /etc/grafana/provisioning/dashboards/hopittydashboards.yaml
ADD hopittyvar.json /var/lib/grafana/dashboards/hopittyvar.json


