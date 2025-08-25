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
├── on_street_curb_management/         # Folder containing download files for dataset
    ├── curbs_downloader.py           # Download Curbs dataset (CSV)
    ├── loading_zones_downloader.py   # Download Loading Zones dataset (CSV)
    ├── on_street_curb_management.py  # Activates all download files
    ├── parking_meters_downloader.py  # Download Parking Meters dataset (CSV)
    ├── truck_routes_downloader.py    # Download Truck Routes dataset (CSV)
├── signals_markings_signs           # Folder for NYC traffic signals, signs, and APS
    ├── accessible_ped_signals_downloader.py   # Download Accessible Pedestrian Signals
    ├── traffic_signal_downloader.py           # Download Traffic Signals (311)
    ├── street_sign_downloader.py              # Download Street Sign Work Orders
    ├── signals_markings_signs.py              # Runs all signal/sign downloaders
├── transit_stop_accessibilty/
    ├── acc_ped_signal_loc_downlaoder.py  # Download Accessible Pedestrian Locations dataset (CSV)
    ├── curbs_downloader.py               # Download Curbs dataset (CSV)
    ├── ped_ramp_locations_downloader.py  # Download Pedestrian Ramp dataset (CSV)
    ├── transit_stop_accessibilty.py      # Orchestrates all download files
├── sidewalk_surface_condition/
    ├── sidewalk_violations_downloader.py # Download Sidewalk violations (CSV)
    ├── tree_damage_downloader.py         # Download Tree damage records (CSV) 
    ├── sidewalk_lot_info_downloader.py   # Download BBL lot info table (CSV with bblid, location, etc.)
    ├── sidewalk_complaints_311_downloader.py   # Download 311 sidewalk complaints (CSV with coordinates)
    ├── sidewalk_geometry_downloader      # Sidewalk polygon geometries (as WKT)
    ├── sidewalk_surface_condition        # Orchestrates all download files  
├── key_destinations/
    ├── issued_licenses_downloader.py      # Download Issued Licenses dataset (CSV)
    ├── key_desinations_downloader.py      # Orchestrates all download files
    ├── nyc_facilities_downloader.py       # Download NYC Facilities dataset (CSV)
├── designed_goods_movement_routes/      # Folder for freight movement routes
    ├── truck_routes.py                  # Download Truck Routes (CSV)
├── environment/
    ├── environment_downloader.py         # Orchestrates all downloads
    ├── heat_vulnerability_downloader.py  # Download Heat Vulnerability dataset (CSV)
    ├── open_space_downloader.py          # Download Open Space dataset (CSV)
    ├── parks_downloader.py               # Download Parks dataset (CSV)
    ├── zipcode_geom_downloader.py        # Download Zipcode Geomertry dataset (CSV)
├── fixed_obstructions/
    ├── fixed_obstructions.py           # Orchestrates all fixed obstruction downloads
    ├── sidewalks_downloader.py         # Download NYC Planimetric Sidewalk dataset (GeoJSON)
    ├── signposts_downloader.py         # Download NYC DOT Street Sign Work Orders dataset (CSV)
    ├── utility_poles_downloader.py     # Download DoITT Telecom Franchise Poles dataset (CSV)
├── bicycle_facilites/
    ├── bike_routes_downloader.py     # Download NYC DOT bicycle facilities dataset (CSV)
├── tree_cover_landscaping/
    ├── tree_cover_landscaping.py             # Orchestrates all tree cover landscaping downloads
    ├── landscaping_downloader.py             # Download NYC Natural Turf Maintenance dataset (CSV)
    ├── nyc_park_zones_downloader.py          # Download NYC Park Zones dataset (GeoJSON)
├── transit_stops_routes/
    ├── transit_stops_routes.py            # Orchestrates all transit stop downloads
    ├── subway_stations_downloader.py      # Download MTA Subway Stations dataset (CSV)
    ├── bus_stop_permits_downloader.py     # Download NYC Intercity Bus Stop Permits dataset (CSV)
├── curb_infrastructure/              # Folder for NYC curb-related features
    ├── curb_infrastructure_downloader.py    # Orchestrator: Runs all curb infrastructure downloaders
    ├── sidewalks_downloader.py              # Download Planimetric Sidewalks dataset
    ├── pedestrian_ramps_downloader.py       # Download Pedestrian Ramp Locations
    ├── raised_crosswalks_downloader.py      # Download Raised Crosswalk Locations
    ├── medians_downloader.py                # Download Planimetric Medians dataset
├── rail_routes_and_crossings/
    ├── rail_routes_and_crossings.py      # Orchestrates all downloads
    ├── crossings_downloader.py           # Download rail crossing points dataset (CSV)
    ├── railroad_lines_downloader.py      # Download railroad lines dataset (CSV)
├── injuries/
    ├── injuries.py                          # Orchestrates all injury-related dataset downloads
    ├── motor_vehicle_crashes_downloader.py  # Download Motor Vehicle Collisions – Crashes dataset (CSV)
    ├── motor_vehicle_persons_downloader.py  # Download Motor Vehicle Collisions – Persons dataset (CSV)
├── Urban_design /
    ├── urban_design_frontage_downlaoder  # Download Urban Design Frontage dataset (CSV)
├── public_open_spaces/
    ├── public_open_spaces.py                 # Orchestrates all public open space dataset processing and integration
    ├── open_space_downloader.py              # Download NYC Planimetric Open Space (Other) dataset (GeoJSON/CSV)
    ├── open_streets_downloader.py            # Download NYC Open Streets dataset (GeoJSON/CSV)
    ├── street_centerline_downloader.py       # Download NYC CSCL Street Centerline dataset (GeoJSON/CSV)
├── land_use/
    ├── land_use.py                        # Orchestrates all land use–related dataset downloads
    ├── facilities_downloader.py           # Download Facilities Database (schools, libraries, civic centers, etc.)
    ├── issued_licenses_downloader.py      # Download Issued Licenses dataset (business licenses across NYC)
    ├── sidewalk_geometry_downloader.py    # Download NYC Planimetric Sidewalk Geometries (polygon base layer)
    ├── nycha_residential_downloader.py    # Download NYCHA Residential Addresses (public housing inventory)
    ├── historic_land_use_downloader.py     # Download Historic Land Use dataset (based on Sanborn maps)
├── transit_ridership
    ├── transit_ridership_orchestrator.py         # Orchestrates all downloads
    ├── ferry_ridership.py                        # Download NYC Ferry Ridership dataset (CSV)
    ├── mta_bus_hourly_ridership_downloader.py    # Download MTA Bus Hourly Ridership dataset (CSV)
    ├── mta_subway_hourly_ridership_downloader.py # Download MTA Subway Hourly Ridership dataset (CSV)
├── social_determinants_of_health
    ├── community_health_survey_downloader.py   # Download NYC Community Health Survey dataset (CSV)
├── bicycle_pedestrian_trip_counts
    ├── bicycle_pedestrian_trip_counts.py            # Orchestrates all downloads
    ├── bicycle_counts_downloader.py                 # Download NYC DOT Bicycle Counts dataset (CSV)
    ├── bicycle_counters_downloader.py               # Download NYC DOT Bicycle Counters dataset (CSV)
    ├── bi_annual_pedestrian_counts_downloader.py    # Download NYC DOT Bi-Annual Pedestrian Counts dataset (CSV)
├── signal_timing_and_phasing
    ├── pedestrian_intervals.py            # Download Pedestrian Signal Intervals dataset (CSV)
├── topography
    ├── elevation_downloader.py       # Download Elevation dataset (CSV)
├── socioeconomic_and_demographic
    ├── demographic_downloader.py             # Download ACS NTA Profile tables (Demographic / Economic / Housing / Social)
    ├── nta_population_downloader.py          # Download NTA population + polygon attributes (geometry, codes, names)
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
python designed_goods_movement_routes/truck_routes.py --output data/designed_goods_movement_routes/truck_routes.csv
python bike_routes_downloader.py -o data/bike_routes.csv
python urban_design_frontage_downloader.py -o data/urban_design.csv
python community_health_survey_downloader.py -o data/community_health_survey.csv
python pedestrian_intervals.py -o data/pedestrian_intervals.csv
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

**Key Destinations:**
The `key_destinations.py` script downloads nyc government facilities and issued licenses data:

```bash
python key_destinations.py   # basic usage
```

Custom output paths:
```bash
python key_destinations_downloader.py \
  --facilities /custom/path/nyc_facilities.csv \
  --licenses /custom/path/issued_licenses.csv
```

**Environments Dataset:**
The `environments_downloader.py` script downloads datasets for heat vulnerability, parks, open spaces, and ZIP code geometries:

```bash
python environments_downloader.py   # basic usage
```

Custom output paths:
```bash
python environment_downloader.py \
  --heat_vulnerability /custom/path/heat_vulnerability.csv \
  --zipcode_geom /custom/path/modzcta.csv \
  --parks /custom/path/parks.csv \
  --open_space /custom/path/open_space.csv
```

**Fixed Obstructions:**
The `fixed_obstructions.py ` script allows downloading multiple datasets simultaneously, including signposts, utility signs and sidewalks.

```bash
python fixed_obstructions.py    # basic usage
```

You can specify custom output paths for each dataset:
```bash
python fixed_obstructions.py \
  --sidewalks /custom/path/sidewalk_planimetric.csv \
  --street_signs /custom/path/street_sign_work_orders.csv \
  --telecom_poles /custom/path/utility_poles.csv
```

**Tree Cover Landscaping:**
The `tree_cover_landscaping.py` script allows downloading multiple datasets simultaneously, including park zones and turf maintenance. 

```bash
python tree_cover_landscaping.py    # basic usage
```

You can specify custom output paths for each dataset:
```bash
python tree_cover_landscaping.py \
  --turf_maintenance custom/path/natural_turf_maintenance.csv \
  --parks_zones custom/path/parks_zones.csv
```

**Transit Stops and Routes:**
The `transit_stops_routes.py ` script downloads subway station data and intercity bus stop permits:

```bash
python transit_stops_routes.py    # basic usage
```

Custom output paths:
```bash
python transit_stops_routes.py \
  --subway_stations /custom/path/subway_stations.csv \
  --intercity_bus_stops /custom/path/intercity_bus_stops.csv
```

**Curb Infrastructure (Sidewalks, crosswalks, driveways, curb ramps, medians, refuges, curb extensions):**
The `curb_infrastructure.py ` script downloads sidewalks, pedestrian ramps, raised crosswalks and medians:

```bash
python curb_infrastructure.py   # basic usage
```

Custom output paths:
```bash
python curb_infrastructure_downloader.py \
  --sidewalks data/curb_infrastructure/sidewalks.csv \
  --pedestrian_ramps data/curb_infrastructure/pedestrian_ramps.csv \
  --raised_crosswalks data/curb_infrastructure/raised_crosswalks.csv \
  --medians data/curb_infrastructure/medians.csv
```

**Rail Routes and Crossings:**
The `rail_routes_and_crossings.py ` script downloads railroads and crossings datasets:

```bash
python rail_routes_and_crossings.py    # basic usage
```

Custom output paths:
```bash
python rail_routes_and_crossings.py \
  --railroads custom/path/railroad_lines.csv \
  --crossings custom/path/rail_crossings_nyc.csv \
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

**Multi Use Paths and Public Open Spaces:**
The `public_open_spaces.py` script downloads and processes open space polygons, open streets, and street centerlines data:

```bash
python public_open_spaces.py  # basic usage
```

Custom output paths:
```bash
python public_open_spaces.py \
  --open_spaces /custom/path/open_spaces.csv \
  --open_streets /custom/path/open_streets.csv \
  --centerlines /custom/path/centerline.csv
```

**Land Use:**
The land_use.py script downloads all datasets related to land use and urban function in NYC, including public facilities, business licenses, and sidewalk geometries.

```bash
python land_use_downloader.py    # basic usage
```

You can specify custom output paths for each dataset:
```bash
python land_use.py \
  --facilities /custom/path/facilities.csv \
  --licenses /custom/path/licenses.csv \
  --sidewalks /custom/path/sidewalks.csv \
  --nycha /custom/path/nycha.csv \
  --historic_land_use /custom/path/historic_land_use.csv
```


**Transit Ridership:**
The `transit_ridership_orchestrator.py` script downloads bus, subway and ferry data:

```bash
python transit_ridership_orchestrator.py   # basic usage
```

You can specify custom output paths for each dataset:
```bash
python transit_ridership_orchestrator.py \
  --subway /custom/mta_subway_hourly_ridership.csv \
  --bus /custom/mta_bus_hourly_ridership.csv \
  --ferry /custom/nyc_ferry_ridership.csv
```

**Bicycle Pedestrian Trip Counts Dataset:**
The `bicycle_pedestrian_trip_counts.py` script orchestrates downloads for bicycle and pedestrian volume datasets from NYC DOT. These include manual/automated bicycle counts, continuous counter data, and semiannual pedestrian counts.

```bash
python bicycle_pedestrian_trip_counts.py   # basic usage
```

Custom output paths:
```bash
python bicycle_pedestrian_trip_counts.py \
  --bicycle_counts /custom/path/bicycle_counts.csv \
  --bicycle_counters /custom/path/bicycle_counters.csv \
  --bi_annual_pedestrian_counts /custom/path/pedestrian_counts.csv
```

**Topography Dataset:**
The `elevation_downloader.py` script downloads building elevation points from the NYC Planimetric Database:

```bash
python elevation_downloader.py    # basic usage
```

Custom output paths:
```bash
python elevation_downloader.py \
  --output /custom/path/elevation_points.csv
```

**Socioeconomic and Demographic Dataset:**
Since one of the datasets is not in a csv form at first there is no orchestrator. There are two downloader files that will download demographic, economic, social and housing profiles. 

```bash
python demographic_downloader.py    # basic usage
python nta_population_downloader.py    # basic usage
```

Custom output paths:
```bash
python demographics_downloader.py \
  --url "URL HERE" \
  --outdir /custom/output/folder/nta_profiles.csv
```

Custom output paths:
```bash
python nta_population_downloader.py \
  --output /custom/path/nta_population.csv
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
