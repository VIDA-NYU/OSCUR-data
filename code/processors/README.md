# Data Processors


This folder contains scripts for post-processing datasets downloaded in `code/downloaders`. Each script is responsible for cleaning, transforming, or formatting a specific dataset before it is uploaded to the Hugging Face repository.

## Folder Structure

```
code/processors/
├── process_speed_humps.py              # Post-processing Speed Humps dataset (CSV)
├── on_street_curb_management.py        # Post-processing On Street Curb Management dataset (CSV)
├── signals_markings_signs.py           # Post-processing Signals Markings and Signs dataset (CSV)
├── transit_stop_accessibilitys.py      # Post-processing Transit Stop Acc dataset (CSV)
├── designed_goods_movement_routes.py   # Post-processing Goods Movement Routes (CSV)
├── README.md                           # This file
└── ...                                 # Add one script per dataset as needed
```

## How to Use/Run

It will depend on the post-processing needed for each dataset:

#### Speed Humps Dataset

```bash
python speed_humps.py -i ../downloaders/data/speed_humps.csv -o processed_data/speed_humps_with_latlon.csv
```
#### Designed Goods Movement Routes Dataset
This script processes the raw dataset for truck routes, adds latitude and longitude points and deletes unecessary columns.

```bash
 python code/processors/designed_goods_movement_routes.py \
  --input data/designed_goods_movement_routes/truck_routes.csv \
  --output data/designed_goods_movement_routes/truck_routes_with_location.csv

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

#### Signals Markings and Signs Dataset

This script integrates street segments with point features such as accessible pedestrian signals, street signs, and traffic signals.
```bash
python signals_markings_signs_processor.py \
  --aps data/signals_markings_signs/accessible_pedestrian_signals.csv \
  --signs data/signals_markings_signs/street_sign_work_orders.csv \
  --signals data/signals_markings_signs/traffic_signals.csv \
  --output processed_data/signals_signs_markings_combined.csv
```

#### Transit Stop Accessibility Dataset
This script joins Accessible Pedestrian Signal (APS) and ramp point data to curb segment linework. The script loads raw CSV data, performs coordinate transformations for accuracy, and executes a nearest-neighbor spatial join. The output is a flat CSV file with accessibility points and their nearest curb segment details.

```bash
python -m code.processors.transit_stop_accessibility \
  --aps   data/transit_stop_accessibility/accessible_pedestrian_signal_locations.csv \
  --ramps data/transit_stop_accessibility/pedestrian_ramp_locations.csv \
  --curbs data/transit_stop_accessibility/nyc_curbs.csv \
  --out   processed_data/transit_stop_accessibility/transit_stop_accessibility_merged.csv
```
 
### Other Datasets
To be added as needed.

## Contributing

To add a new processor:

1. Add a `Python` script in [code/processors](./) to clean, transform, or reformat the dataset.
   - If multiple scripts are needed for one dataset, organize them in a subdirectory named after the dataset ID or source (e.g., `code/processors/your_dataset_id/`).
2. Add CLI usage instructions and a brief description of the processing to this `README.md`.

---
