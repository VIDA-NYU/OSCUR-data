# Data Downloaders

This folder contains Python scripts to **automatically download and save raw data** from various public data sources, including NYC Open Data and others. 

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
├── README.md                         # This file
└── ...                               # Add one script per dataset as needed
```

## Requirements

- Python 3.7+
- `requests` module
- Additional dependencies may be required depending on the dataset (e.g., `pandas`, `pyarrow` for Parquet)

Install basic dependencies with:

```bash
pip install requests
```

## How to Use

Each script accepts the following standardized arguments:
- `-o` or `--output`: **Required** - Specify the output file path
- `--app-token`: *Optional* - Socrata API app token to avoid rate limits
- `--timeout`: *Optional* - Request timeout in seconds (default: 10)

Ensure the `data/` folder exists:

```bash
mkdir -p data
```

> 🔒 **Note:** The `data/` folder will not be committed to this repository. Instead, all collected data will be uploaded to a Hugging Face dataset repository for sharing and versioning. If needed, post-processing and format conversions should be handled in [code/processors](./).

### Example usage:

**Basic usage:**
```bash
python speed_humps.py -o data/speed_humps.csv
python raised_crosswalks.py -o data/raised_crosswalks.csv
python NYC_vehicle_collisions.py -o data/NYC_vehicle_collisions.csv
python nyc_311.py -o data/nyc_311.csv
```

**With API token and custom timeout:**
```bash
python speed_humps.py -o data/speed_humps.csv --app-token YOUR_TOKEN --timeout 30
```

**Get help for any downloader:**
```bash
python speed_humps.py --help
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
