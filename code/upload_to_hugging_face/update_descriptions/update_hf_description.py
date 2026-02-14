#!/usr/bin/env python3
"""
update_hf_description.py

Utility functions to fetch dataset descriptions from YAML metadata files
and update the README.md (dataset card) on the Hugging Face Hub.
"""

import sys
import yaml
import requests
from huggingface_hub import HfApi, HfFileSystem
from pathlib import Path
import io

def get_description_from_yaml(yaml_url: str) -> str:
    """Fetch YAML file from a URL and extract the 'description' field."""
    try:
        response = requests.get(yaml_url)
        response.raise_for_status()
        metadata = yaml.safe_load(response.text)
        description = metadata.get("description", "No description found in YAML file.")
        return description.strip()
    except Exception as e:
        print(f"⚠️ Error fetching {yaml_url}: {e}")
        return "No description available (fetch error)."

def update_dataset_description(repo_id: str, new_description: str, token: str):
    """
    Update or add the 'description' field in a dataset README.md on Hugging Face Hub.
    """
    api = HfApi()
    fs = HfFileSystem()

    # Path to README in the dataset repo
    readme_path = f"datasets/{repo_id}/README.md"
    
    # --- Fetch existing README.md content ---
    try:
        with fs.open(readme_path, "r") as f: # Read existing README.md content from the hub
            content = f.read()
    except FileNotFoundError:
        content = ""

    # --- Split YAML metadata (front matter) and Markdown body ---
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            yaml_block = parts[1]
            markdown_body = parts[2].lstrip()
            metadata = yaml.safe_load(yaml_block) or {}
        else:
            metadata = {}
            markdown_body = content
    else:
        metadata = {}
        markdown_body = content

    # --- Update description in YAML metadata ---
    metadata["description"] = new_description

    # --- Rebuild the README.md ---
    new_yaml = yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True)
    updated_readme = f"---\n{new_yaml}---\n\n{markdown_body}"

    # --- Upload the new README.md back to the Hub ---
    # api.upload_file(
    #     path_or_fileobj=io.BytesIO(updated_readme.encode("utf-8")),
    #     path_in_repo="README.md",
    #     repo_id=repo_id,
    #     repo_type="dataset",
    #     token=token,
    #     commit_message="Update dataset description programmatically",
    # )

    print(f"\n📘 Processing {repo_id} → {yaml_file}")
    print(f"   Description length: {len(new_description)} chars")
    print(f"✅ Updated description for {repo_id}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python update_hf_description.py <dataset_yaml> <hf_token>")
        sys.exit(1)

    dataset_yaml = Path(sys.argv[1])
    hf_token = sys.argv[2]

    with open(dataset_yaml, "r") as f:
        dataset_map = yaml.safe_load(f)

    for repo_id, yaml_file in dataset_map.items():
        yaml_url = f"https://raw.githubusercontent.com/VIDA-NYU/OSCUR-data/main/metadata/{yaml_file}"
        desc = get_description_from_yaml(yaml_url)
        update_dataset_description(repo_id, desc, hf_token)

# if __name__ == "__main__":
#     # Allow command-line execution
#     if len(sys.argv) != 4:
#         print("Usage: python update_hf_description.py <repo_id> <yaml_url> <hf_token>")
#         sys.exit(1)

#     repo_id, yaml_url, token = sys.argv[1:]
#     desc = get_description_from_yaml(yaml_url)
#     update_dataset_description(repo_id, desc, token)

