# Data Downloaders

This folder contains Python scripts to **automatically download and save raw data** from various public data sources, including NYC Open Data and others. These data will be used later by a [processor]([code/processors](./)) to generate the target dataset.

The downloaders use a **base class architecture** to ensure consistency, maintainability, and code reusability across all dataset downloaders.

## Architecture

All NYC Open Data downloaders inherit from a common base class (`NYCDataDownloader`) that provides:
- Standardized command-line interface
- Consistent error handling and status reporting
- Session management with optional API token support
- Configurable timeout settings
- Unified download logic

This architecture ensures that all downloaders behave consistently and makes adding new downloaders simple and reliable.

## Folder Structure

```
code/downloaders/
├── nyc_base_downloader.py            # Base class for all NYC Open Data downloaders
├── speed_humps.py                    # Download Speed Humps dataset (CSV)
├── raised_crosswalks.py              # Download Raised Crosswalks dataset (CSV)
├── NYC_vehicle_collisions.py         # Download Vehicle Collisions (Crashes) dataset (CSV)
├── nyc_311.py                        # Download NYC 311 Requests dataset (CSV)
├── on_street_curb_management         # Folder containing download files for dataset
    ├── curbs_downloader.py           # Download Curbs dataset (CSV)
    ├── loading_zones_downloader.py   # Download Loading Zones dataset (CSV)
    ├── on_street_curb_management.py  # Activates all download files
    ├── parking_meters_downloader.py  # Download Parking Meters dataset (CSV)
    ├── truck_routes_downloader.py    # Download Truck Routes dataset (CSV)
├── signals_markings_signs/           # Folder for NYC traffic signals, signs, and APS
    ├── accessible_ped_signals_downloader.py   # Download Accessible Pedestrian Signals
    ├── traffic_signal_downloader.py           # Download Traffic Signals (311)
    ├── street_sign_downloader.py              # Download Street Sign Work Orders
    ├── signals_markings_signs.py              # Runs all signal/sign downloaders
├── transit_stop_accessibilty.py/
   ├── acc_ped_signal_loc_downlaoder.py  # Download acc ped location dataset (CSV)
   ├── curbs_downloader.py               # Download curbs dataset (CSV)
   ├── ped_ramp_locations_downloader.py  # Download pedestrian ramp dataset (CSV)
   ├── transit_stop_accessibilty.py      # Orchestrates all downloads
├── injuries/
    ├── injuries.py                          # Orchestrates all injury-related dataset downloads
    ├── motor_vehicle_crashes_downloader.py  # Download Motor Vehicle Collisions – Crashes dataset (CSV)
    ├── motor_vehicle_persons_downloader.py  # Download Motor Vehicle Collisions – Persons dataset (CSV)
├── README.md                         # This file
└── ...                               # Add one script per dataset as needed
```

## How to Use

Ensure the `data/` folder exists:

```bash
mkdir -p data
```

> 🔒 **Note:** The `data/` folder will not be committed to this repository. If needed, post-processing and format conversions should be handled in [code/processors](./), and the processed data will be uploaded to a Hugging Face dataset repository for sharing.


#### Single Dataset Download
Each script accepts the following standardized arguments:
- `-o` or `--output`: **Required** - Specify the output file path
- `--app-token`: *Optional* - Socrata API app token to avoid rate limits
- `--timeout`: *Optional* - Request timeout in seconds (default: 10)

Basic usage:
```bash
python speed_humps.py -o data/speed_humps.csv
python raised_crosswalks.py -o data/raised_crosswalks.csv
python NYC_vehicle_collisions.py -o data/NYC_vehicle_collisions.csv
python nyc_311.py -o data/nyc_311.csv
```
With API token and custom timeout:
```bash
python speed_humps.py -o data/speed_humps.csv --app-token YOUR_TOKEN --timeout 30
```

Get help for any downloader:
```bash
python speed_humps.py --help
```

#### Multiple Datasets Download (Simultaneous)

Some datasets require multiple related files to generate the target dataset. We provide scripts that download multiple datasets simultaneously.

**On street curb management dataset:** 
The `on_street_curb_management.py` script download curbs, loading zones, parking meters, and truck routes data:
```bash
python on_street_curb_management.py  # basic usage
```

By default, the datasets will be saved to the following paths:
- `data/on_street_curb_management/curbs.csv`
- `data/on_street_curb_management/loading_zones.csv`
- `data/on_street_curb_management/parking_meters.csv`
- `data/on_street_curb_management/truck_routes.csv`

You can specify custom output paths for each dataset:
```bash
python on_street_curb_management.py \
  --curbs /custom/path/curbs.csv \
  --loading_zones /custom/path/loading_zones.csv \
  --parking_meters /custom/path/parking_meters.csv \
  --truck_routes /custom/path/truck_routes.csv
```

**Signals, Markings, and Signs Dataset:**
The `signals_markings_signs.py` script downloads accessible pedestrian signals, traffic signals, and street sign work orders data:

```bash
python signals_markings_signs.py   # basic usage
```

Custom output paths:
```bash
python signals_markings_signs.py \
  --accessible_pedestrian_signals /custom/path/aps.csv \
  --traffic_signals /custom/path/traffic.csv \
  --street_sign_work_orders /custom/path/signs.csv
```

**Transit Stop Accessibility Dataset:**
The `transit_stop_accessibility.py` script downloads Accessible Pedestrian Signal (APS) locations, pedestrian-ramp locations, and the NYC Planimetric Curbs layer to support multimodal transportation planning:

```bash
python -m code.downloaders.transit_stop_accessibility.transit_stop_accessibility  # basic usage
```

By default, the datasets will be saved to the following paths:
- `data/transit_stop_accessibility/accessible_ped_signal_locations.csv`
- `data/transit_stop_accessibility/pedestrian_ramp_locations.csv`
- `data/transit_stop_accessibility/curbs.csv`

You can specify custom output paths for each dataset:
```bash
python -m code.downloaders.transit_stop_accessibility.transit_stop_accessibility \
  --aps /custom/path/acc_ped_signal_loc.csv \
  --ramps /custom/path/ped_ramp_loc.csv \
  --curbs /custom/path/curbs.csv
```

**Sidewalk Surface Condition Dataset:**
The `sidewalk_surface_condition.py` script allows downloading multiple datasets simultaneously, including complaints, violations, lot info, tree damage and sidewalks.

```bash
python sidewalk_surface_condition.py
```

By default, the datasets will be saved to the following paths:
- `data/sidewalk_surface_condition/sidewalk_complaints_311.csv`
- `data/sidewalk_surface_condition/sidewalk_violations.csv`
- `data/sidewalk_surface_condition/sidewalk_lot_info.csv`
- `data/sidewalk_surface_condition/tree_damage.csv`
- `data/sidewalk_surface_condition/sidewalk_planimetric.csv`

You can specify custom output paths for each dataset:
```bash
python sidewalk_surface_condition.py \
  --violations /custom/path/sidewalk_violations.csv \
  --tree_damage /custom/path/tree_damage.csv \
  --complaints_311 /custom/path/sidewalk_311_complaints.csv \
  --planimetric /custom/path/sidewalk_planimetric.csv \
  --lot_info /custom/path/lot_info.csv
```

**Injuries, injury severity, and near misses:**
The `injuries.py` script downloads motor vehicle crahses and persons involved in crash data:

```bash
python injuries.py   # basic usage
```

Custom output paths:
```bash
python injuries.py \
  --motor_vehicle_crashes /custom/path/motor_vehicle_crashes.csv \
  --motor_vehicle_persons /custom/path/motor_vehicle_persons.csv
```

## Base Class Benefits

The shared base class architecture provides several advantages:

- **Consistency**: All downloaders have identical interfaces and behavior
- **Maintainability**: Common functionality is centralized in one place
- **Reliability**: Standardized error handling and request management
- **Extensibility**: Adding new NYC dataset downloaders requires minimal code
- **Features**: All downloaders automatically inherit new capabilities added to the base class

## Notes

- Datasets vary in size and format; some may require significant memory or filtering.
- Downloaders are designed to be minimal, focusing on retrieving raw data.
- All NYC Open Data downloaders follow the same URL pattern and use Socrata's CSV export endpoints.

## Contributing

### Adding a new NYC Open Data downloader:

1. Create a new Python script that imports and inherits from `NYCDataDownloader`:
   ```python
   from nyc_base_downloader import NYCDataDownloader
   
   class YourDatasetDownloader(NYCDataDownloader):
       BASE_URL = "https://data.cityofnewyork.us/resource/your-id.csv"
       DATASET_NAME = "Your Dataset Name"
   
   def main():
       downloader = YourDatasetDownloader()
       downloader.run()
   
   if __name__ == "__main__":
       main()
   ```

2. Add usage instructions to this `README.md`.

### Adding non-NYC data sources:

1. For other data sources, create appropriate base classes or standalone scripts as needed.
2. If multiple scripts are needed for one dataset, organize them in a subdirectory named after the dataset ID or source (e.g., `code/downloaders/your_dataset_id/`).
3. Ensure your script handles the dataset's specific format and retrieval method.

---
