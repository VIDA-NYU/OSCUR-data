
# Data Processors


This folder contains scripts for post-processing datasets downloaded in `code/downloaders`. Each script is responsible for cleaning, transforming, or formatting a specific dataset before it is uploaded to the Hugging Face repository.

## Folder Structure

```
code/processors/
├── process_speed_humps.py       # Post-processing Speed Humps dataset (CSV)
├── signals_markings_signs.py    # Post-processing Signals Markings and Signs dataset (CSV)
├── README.md                    # This file
└── ...                          # Add one script per dataset as needed
```

## How to Use

It will depend on the post-processing needed for each dataset. Examples:

### Speed Humps Dataset

This script reads the raw Speed Humps dataset and extracts latitude and longitude from the `the_geom` column. These coordinates are added as new columns and saved in a new CSV file.

**How to run:**

```bash
python process_speed_humps.py -i ../downloaders/data/speed_humps.csv -o ../downloaders/data/speed_humps_with_latlon.csv
```

**How to run for multiple sources:**

```bash
python signals_markings_signs_processor.py \
  --aps data/signals_markings_signs/accessible_pedestrian_signals.csv \
  --signs data/signals_markings_signs/street_sign_work_orders.csv \
  --signals data/signals_markings_signs/traffic_signals.csv \
  --output data/signals_markings_signs/signals_signs_markings_combined.csv
```

### Other Datasets
To be added as needed.

## Contributing

To add a new processor:

1. Add a `Python` script in [code/processors](./) to clean, transform, or reformat the dataset.
   - If multiple scripts are needed for one dataset, organize them in a subdirectory named after the dataset ID or source (e.g., `code/processors/your_dataset_id/`).
2. Add CLI usage instructions and a brief description of the processing to this `README.md`.

---
