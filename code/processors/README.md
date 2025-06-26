# Data Processors


This folder contains scripts for post-processing datasets downloaded in `code/downloaders`. Each script is responsible for cleaning, transforming, or formatting a specific dataset before it is uploaded to the Hugging Face repository.

## Folder Structure

```
code/processors/
├── process_speed_humps.py             # Post-processing Speed Humps dataset (CSV)
├── on_street_curb_management.py       # Post-processing On Street Curb Management dataset (CSV)
├── README.md                          # This file
└── ...                                # Add one script per dataset as needed
```

## How to Use/Run

It will depend on the post-processing needed for each dataset:

#### Speed Humps Dataset

```bash
python speed_humps.py -i ../downloaders/data/speed_humps.csv -o processed_data/speed_humps_with_latlon.csv
```

#### On-Street Curb Management Dataset

This script processes the raw datasets for curbs, parking meters, loading zones, and truck routes, merging them into a unified dataset.
```bash
python on_street_curb_management.py \
  --curbs ../downloaders/data/on_street_curb_management/curbs.csv \
  --loading_zones ../downloaders/data/on_street_curb_management/loading_zones.csv \
  --parking_meters ../downloaders/data/on_street_curb_management/parking_meters.csv \
  --truck_routes ../downloaders/data/on_street_curb_management/truck_routes.csv \
  --output processed_data/on_street_curb_management.csv
```

### Other Datasets
To be added as needed.

## Contributing

To add a new processor:

1. Add a `Python` script in [code/processors](./) to clean, transform, or reformat the dataset.
   - If multiple scripts are needed for one dataset, organize them in a subdirectory named after the dataset ID or source (e.g., `code/processors/your_dataset_id/`).
2. Add CLI usage instructions and a brief description of the processing to this `README.md`.

---
