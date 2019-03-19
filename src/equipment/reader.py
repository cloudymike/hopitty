import yaml
with open('grain3g.yaml') as f:
    # use safe_load instead load
    dataMap = yaml.safe_load(f)

print dataMap
