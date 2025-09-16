<div align="center">
   <h1>OSCUR data</h1>
   <p>
      <img src="https://img.shields.io/static/v1?label=HuggingFace&message=oscur&color=FFD21E&style=for-the-badge&logo=huggingface&logoColor=white" alt="HuggingFace oscur">
      <img src="https://img.shields.io/static/v1?label=Python&message=3.8%2B&color=3776AB&style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+">
   </p>
</div>

---
# Overview

This repository presents a comprehensive framework for collecting, documenting, and analyzing urban transportation datasets, with a focus on New York City data sources. It integrates spatial data science theory with practical implementation aligned with U.S. Department of Transportation (DOT) data standards.

This repository tracks the progress of data generation and enhancement. The goal is to generate geospatial datasets across three key categories: **Infrastructure**, **Traveler Behavior/Safety**, and **Context**, to support decision-making tools for multimodal transportation planning. For detailed progress tracking, refer to the [GitHub issue](https://github.com/VIDA-NYU/csai-datagathering/issues/1).

🤗 All datasets uploaded are available on our **[HuggingFace Hub](https://huggingface.co/oscur)**.  


## Repository Structure

```
OSCUR-data/
├── metadata/                 # YAML specifications describing each data source
├── code/                     # Scripts to download, process, and upload data
│   ├── metadata_generators/     # Generate standardized metadata YAML files
│   ├── downloaders/             # Raw data acquisition from various APIs
│   ├── processors/              # Data cleaning, transformation, and validation
│   └── upload_to_hugging_face/  # Utilities for uploading datasets to Hugging Face
├── data_profiles/            # JSON summaries/statistics of datasets
└── examples/                 # Jupyter notebooks demonstrating dataset usage
```

## Add a New Dataset

To contribute a new dataset to this repository, follow these steps:

**1. Metadata**

- Store dataset metadata as individual ``YAML`` files in the [metadata/](./metadata) directory.
- Refer to the guide in [code/metadata_generators](./code/metadata_generators/) for how to create or generate a metadata file.
- Ensure all required metadata fields (e.g., title, description, source, license) are completed.


**2. Code**
- **Metadata Generators:**
   - Add or modify scripts in [code/metadata_generators](./code/metadata_generators/) to generate standardized YAML metadata files.
   - These scripts can use NYC Open Data APIs or other APIs to extract metadata and save it in the [metadata/](./metadata) directory.

- **Downloaders:**
   - Add a ``Python`` script that collects raw data from the source to [code/downloaders](./code/downloaders/).
   - If multiple scripts are needed, create a subdirectory named after the dataset ID (e.g., ``code/downloaders/your_dataset_id/``).

- **Processors:**
   - Add a ``Python`` script for cleaning, transforming, and validating the data to [code/processors](./code/processors/).
   - If necessary, group related scripts under a folder named after the dataset ID.

- **Uploader:**
   - Upload your cleaned dataset to the [OSCUR HuggingFace Hub](https://huggingface.co/oscur) repository.
   - Follow the guide in [code/upload_to_hugging_face/README.md](code/upload_to_hugging_face/README.md) for instructions.

**3. Data Profile**

Generate a profile summary of the dataset (recommended: use [``datamart-profiler``](https://pypi.org/project/datamart-profiler/), [usage examples](https://gitlab.com/ViDA-NYU/auctus/auctus/-/blob/master/examples/profile.ipynb?ref_type=heads)) and save it as a ``.json`` file in [data_profiles/](./data_profiles).
Note: The data profile JSON file must include both plots and sample data. To ensure this, set the `include_sample` and `plots` parameters to `True` when generating the profile.
```
import datamart_profiler
metadata = datamart_profiler.process_dataset(df, include_sample=True, plots=True)
```


**4. Usage Example**
   - Provide a ``Jupyter notebook`` demonstrating how to use or visualize the dataset.
   - Save it to [examples/](./examples).

## Contributing

We welcome contributions to enhance the dataset collection and improve the tools! Please:
- Check the [GitHub issue](https://github.com/VIDA-NYU/csai-datagathering/issues/1) for current progress and to avoid duplicating efforts.
- Submit pull requests with new datasets, scripts, or documentation updates.

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.
