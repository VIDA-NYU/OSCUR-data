import argparse
from datasets import load_dataset, Dataset, Features, Value
import pandas as pd
import os
import csv
import datasets
from huggingface_hub import HfApi, create_repo, login
import datamart_profiler  # Import datamart-profiler

# Mapping dictionary
TYPE_MAPPING = {
    'https://metadata.datadrivendiscovery.org/types/MissingData': None,     # Handle missing data as None
    'http://schema.org/Integer': 'int64',
    'http://schema.org/Float': 'float64',
    'http://schema.org/Text': 'string',
    'http://schema.org/Boolean': 'bool',
    'http://schema.org/DateTime': 'string',
    'http://schema.org/address': 'string',
    'http://schema.org/AdministrativeArea': 'string',
    'http://schema.org/URL': 'string',
    'https://metadata.datadrivendiscovery.org/types/FileName': 'string',
    'http://schema.org/identifier': 'string',
    'http://schema.org/Enumeration': 'string',
    'http://schema.org/GeoCoordinates': 'string',
    'http://schema.org/GeoShape': 'string'
}

from datasets import Features, Value, ClassLabel, Sequence

def generate_features_from_profile(profile):
    """
    Generate Hugging Face Datasets features schema from datamart-profiler profile.
    
    Args:
        profile (dict): Datamart profiler JSON profile with 'columns' key.
    
    Returns:
        datasets.Features: Hugging Face features schema.
    """
    columns = profile['columns']
    features = {}

    for column in columns:
        column_name = column['name']
        structural_type = column['structural_type']

        hf_type = TYPE_MAPPING.get(structural_type, 'string')

        # if hf_type == 'ClassLabel':
        #     # Try to get categories from profile's 'categories' or 'distinct_values'
        #     # Fallback to empty list if unavailable
        #     categories = column.get('categories')
        #     if categories is None:
        #         # Sometimes distinct_values is available
        #         categories = column.get('distinct_values', [])
        #     if categories and isinstance(categories, list):
        #         features[column_name] = ClassLabel(names=[str(cat) for cat in categories])
        #     else:
        #         # Default fallback if no categories info is available
        #         features[column_name] = ClassLabel(names=[])
        
        # elif hf_type == 'dict':
        #     # For GeoCoordinates or GeoShape, assume dict with string keys and float values (lat/lon)
        #     # Customize as needed. Here we define a nested feature schema for geo points:
        #     features[column_name] = Features({
        #         "latitude": Value("float64"),
        #         "longitude": Value("float64")
        #     })
        
        if hf_type in ['int64', 'float64', 'string', 'bool']:
            features[column_name] = Value(hf_type)
        
        else:
            # fallback for any unknown type
            features[column_name] = Value("string")
    
    return Features(features)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Upload CSV to Hugging Face Hub")
parser.add_argument("--token", required=True, help="Hugging Face token")
parser.add_argument("--organization", required=True, help="Hugging Face organization name")
parser.add_argument("--repo_name", required=True, help="Repository name")
parser.add_argument("--csv_filename", required=True, help="Path to the CSV file")
args = parser.parse_args()

# Use the arguments
token_value = args.token
organization = args.organization
repo_name = args.repo_name
csv_filename = args.csv_filename
repo_id = f"{organization}/{repo_name}"

# Login to Hugging Face
login(token=token_value)
api = HfApi()

# Create the repository only if it doesn't already exist
try:
    create_repo(repo_id, repo_type="dataset", exist_ok=True)
    print(f"Repository '{repo_id}' is ready.")
except Exception as e:
    print(f"An error occurred while creating the repository: {e}")

try:
    # Attempt to load the dataset directly from the CSV file
    dataset = Dataset.from_csv(csv_filename)
except Exception as e1:
    # If the first attempt fails, print the error and try to load it using pandas
    print(f"First attempt Failed to create dataset from CSV file: {e1}")
    try:
        # Second attempt to create the dataset using pandas
        df_data = pd.read_csv(csv_filename)
        dataset = Dataset.from_pandas(df_data)
    except Exception as e2:
        print(f"Second attempt to create dataset from pandas DataFrame failed: {e2}")
        try:
            # Third Attempt: Use datamart-profiler to infer column types
            # df_data = pd.read_csv(csv_filename)
            # df_data = pd.read_csv(csv_filename, dtype=str)  # Force all columns to string type
            df_data = pd.read_csv(csv_filename)
            profile = datamart_profiler.process_dataset(csv_filename)
            features = generate_features_from_profile(profile)
            dataset = Dataset.from_pandas(df_data, features=features)
        except Exception as e3:
            print(f"Third attempt: Failed to create dataset from CSV file with datamart-profiler: {e3}")
            try:
                # Fourth Attempt: Use csv.DictReader to infer fieldnames and generate features
                csv_path = os.path.join(os.path.dirname(csv_filename), os.path.basename(csv_filename))
                with open(csv_path, newline="", encoding="utf-8") as csvfile:
                    reader = csv.DictReader(csvfile)
                    fieldnames = reader.fieldnames
                features = datasets.Features({
                    **{col: datasets.Value("string") for col in fieldnames}
                })
                dataset = Dataset.from_csv(csv_filename, features=features)
            except Exception as e4:
                print(f"Fourth attempt: Failed to create dataset from CSV file using csv.DictReader: {e4}")
                raise

# Push the CSV file directly to the repository
try:
    api.upload_file(
        path_or_fileobj=csv_filename,
        path_in_repo=os.path.basename(csv_filename),
        repo_id=repo_id,
        repo_type="dataset"
    )
    print(f"CSV file '{csv_filename}' has been pushed to the repository.")
except Exception as e:
    print(f"An error occurred while pushing the CSV file: {e}")

# Upload the profiling JSON data to the repository
try:
    import json
    profile = datamart_profiler.process_dataset(csv_filename, include_sample=True, plots=True)
    profile_json = json.dumps(profile, indent=4)
    profile_filename = "profiling_metadata.json"
    api.upload_file(
        path_or_fileobj=profile_json.encode("utf-8"),  # Convert JSON string to bytes
        path_in_repo=profile_filename,
        repo_id=repo_id,
        repo_type="dataset"
    )
    print(f"Profiling JSON data has been uploaded to the repository as '{profile_filename}'.")
except Exception as e_upload:
    print(f"An error occurred while uploading the profiling JSON data: {e_upload}")

# Push the dataset to the repository
dataset.push_to_hub(repo_id)