# Ingress YAML Converter (v1beta1 to v1)

This Python script converts Kubernetes Ingress resources from the deprecated v1beta1 version to the current stable v1 version. It also updates relevant Kustomization files for consistency.

## Usage

1. Clone this repository.
2. Navigate to the cloned directory.
3. Run the script using the following command:

   ```bash
   python convert_ingress.py <path_to_directory>
   ```

   Replace `<path_to_directory>` with the path to the directory containing your Ingress YAML files and Kustomization files.

## What the script does:

- Scans the specified directory for YAML files and Kustomization files.
- For each Ingress YAML file:
    - Checks if it's in v1beta1 format.
    - If so, updates the `apiVersion` to `networking.k8s.io/v1`.
    - Adds missing `path` fields in rules.
    - Adjusts the backend structure to match v1 format.
    - Adds `pathType` fields if missing.
- For each Kustomization file:
    - Updates Ingress version references in patches to `v1`.

## Important notes:

- The script modifies files in place. It's recommended to create a backup of your files before running the script.
- Thoroughly test the converted files in a non-production environment before deploying them.
- Consider using a version control system to track changes made by the script.

## Contributions

Pull requests are welcome! Please ensure your code follows the project's style and conventions.

## Author

Davide Prette 
