import yaml

yaml_path = './Dataset/data.yaml'

def parse_yaml():
    # Read the YAML content from the file
    with open(yaml_path, 'r') as file:
        yaml_content = yaml.safe_load(file)

    return yaml_content

def update_yaml(new_data):
    # Write updated data back to the file
    with open(yaml_path, 'w') as file:
        yaml.dump(new_data, file)
