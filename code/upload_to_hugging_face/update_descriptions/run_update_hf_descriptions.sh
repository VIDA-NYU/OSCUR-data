#!/bin/bash
# Usage:
#   bash run_update_hf_descriptions.sh <hf_token>

HF_TOKEN=$1

if [ -z "$HF_TOKEN" ]; then
  echo "Usage: bash run_update_hf_descriptions.sh <hf_token>"
  exit 1
fi

# Define dataset–YAML pairs
declare -A DATASETS
DATASETS["oscur/NYC_vehicle_collisions_issue"]="https://raw.githubusercontent.com/VIDA-NYU/OSCUR-data/main/metadata/NYC_vehicle_collisions.yaml"
DATASETS["oscur/NYC_ferry_ridership"]="https://raw.githubusercontent.com/VIDA-NYU/OSCUR-data/main/metadata/NYC_ferry_ridership.yaml"

# Run the Python updater for each dataset
for repo_id in "${!DATASETS[@]}"; do
  yaml_url="${DATASETS[$repo_id]}"
  echo "➡️ Updating $repo_id ..."
  python3 update_hf_description.py "$repo_id" "$yaml_url" "$HF_TOKEN"
done
