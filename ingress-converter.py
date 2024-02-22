import yaml
import sys
import os

def convert_ingress_v1beta_to_v1(file_path):
    with open(file_path, 'r') as file:
        try:
            data = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML in file {file_path}: {exc}")
            return

    if data is None or data.get('apiVersion') != 'networking.k8s.io/v1beta1':
        return  # Skip non-v1beta1 files or empty files

    # Update the apiVersion
    data['apiVersion'] = 'networking.k8s.io/v1'
    # Check for missing path in each rule and add it if missing
    for rule in data.get("spec", {}).get("rules", []):
        if "http" in rule:
            for path in rule["http"].get("paths", []):
                if "path" not in path:
                    path["path"] = "/"

    # Handle changes in the backend structure and add pathType
    for rule in data.get('spec', {}).get('rules', []):
        for path in rule.get('http', {}).get('paths', []):
            backend = path.get('backend', {})
            if 'serviceName' in backend and 'servicePort' in backend:
                path['backend'] = {
                    'service': {
                        'name': backend['serviceName'],
                        'port': {
                            'number': backend['servicePort']
                        }
                    }
                }
                backend.pop('serviceName', None)
                backend.pop('servicePort', None)

            if 'pathType' not in path:
                path['pathType'] = 'Prefix'

    # Overwrite the original file with the modified data
    with open(file_path, 'w') as file:
        yaml.dump(data, file, sort_keys=False)
    print(f"Converted and updated file: {file_path}")

def update_kustomization_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    if 'patchesJson6902' in data:
        for patch in data['patchesJson6902']:
            if patch['target'].get('kind') == 'Ingress' and patch['target'].get('version') == 'v1beta1':
                patch['target']['version'] = 'v1'

        with open(file_path, 'w') as file:
            yaml.dump(data, file, sort_keys=False)
        print(f"Updated kustomization file: {file_path}")

def convert_all_ingress_in_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file == 'kustomization.yaml':
                update_kustomization_yaml(file_path)
            elif file.endswith('.yaml') or file.endswith('.yml'):
                convert_ingress_v1beta_to_v1(file_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_ingress.py <path_to_directory>")
        sys.exit(1)

    convert_all_ingress_in_directory(sys.argv[1])
