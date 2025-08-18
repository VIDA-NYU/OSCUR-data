# Data Processors


This folder contains scripts for post-processing datasets downloaded in `code/downloaders`. Each script is responsible for cleaning, transforming, or formatting a specific dataset before it is uploaded to the Hugging Face repository.

## Folder Structure

```
code/processors/
├── process_speed_humps.py             # Post-processing Speed Humps dataset (CSV)
├── on_street_curb_management.py       # Post-processing On Street Curb Management dataset (CSV)
├── signals_markings_signs.py          # Post-processing Signals Markings and Signs dataset (CSV)
├── transit_stop_accessibilitys.py     # Post-processing Transit Stop Acc dataset (CSV)
├── sidewalk_surface_condition.py      # Post-processing Sidewalk Surface Condition dataset (CSV)
├── designed_goods_movement_routes.py  # Post-processing Goods Movement Routes (CSV)
├── merge_hvi_zipcode_geom.py          # Post-processing Environment dataset (CSV)
├── fixed_obstructions.py              # Post-processing Fixed Obstructions dataset (CSV)
├── tree_cover_landscaping.py          # Post-processing Tree Cover and Landscaping dataset (CSV)
├── curb_infrastructure.py             # Post-processing Curb Infrastructure dataset (CSV)
├── rail_routes_and_crossings.py       # Post-processing Rail Routes and Crossings dataset (CSV)
├── public_open_spaces.py              # Post-processing Public Open Spaces dataset (CSV)
├── land_use.py                        # Post-processing Land Use dataset (CSV)
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

#### Signals Markings and Signs Dataset

This script integrates street segments with point features such as accessible pedestrian signals, street signs, and traffic signals.
```bash
python signals_markings_signs_processor.py \
  --aps ../downloaders/data/signals_markings_signs/accessible_pedestrian_signals.csv \
  --signs ../downloaders/data/signals_markings_signs/street_sign_work_orders.csv \
  --signals ../downloaders/data/signals_markings_signs/traffic_signals.csv \
  --output processed_data/signals_signs_markings_combined.csv
```

#### Transit Stop Accessibility Dataset
This script joins Accessible Pedestrian Signal (APS) and ramp point data to curb segment linework. The script loads raw CSV data, performs coordinate transformations for accuracy, and executes a nearest-neighbor spatial join. The output is a flat CSV file with accessibility points and their nearest curb segment details.

```bash
python -m code.processors.transit_stop_accessibility \
  --aps   ../downloaders/data/transit_stop_accessibility/accessible_pedestrian_signal_locations.csv \
  --ramps ../downloaders/data/transit_stop_accessibility/pedestrian_ramp_locations.csv \
  --curbs ../downloaders/data/transit_stop_accessibility/nyc_curbs.csv \
  --out   processed_data/transit_stop_accessibility/transit_stop_accessibility_merged.csv
```

#### Sidewak Surface Condition (2 merge scripts)
This script processes the raw datasets for sidewalks, complaints, violations, tree damage and lot info, merging them into a unified dataset.
```bash
python merge_sidewalk_datasets.py \
  --violations ../downloaders/data/sidewalk_surface_condition/sidewalk_violations.csv \
  --tree_damage ../downloaders/data/sidewalk_surface_condition/tree_damage.csv \
  --lot_info ../downloaders/data/sidewalk_surface_condition/lot_info.csv \
  --out ../processors/processed_data/sidewalk_surface_violations_and_trees.csv
```

```bash
python merge_geocoded_and_311.py \
  --geocoded ../processors/processed_data/sidewalk_surface_violations_and_trees.csv \
  --complaints_311 ../downloaders/data/sidewalk_surface_condition/sidewalk_311_complaints.csv \
  --sidewalk_geom ../downloaders/data/sidewalk_surface_condition/sidewalk_planimetric.csv \
  --out ../processors/processed_data/sidewalk_surface_full_merged.csv
```

#### Key Destinations
No postprocessing script is needed, as the original datasets are being preserved without any merging.

#### Designed Goods Movement Routes Dataset
This script processes a CSV of NYC truck routes by extracting longitude and latitude from the geometry column, keeps selected relevant columns, and saves the cleaned data to a new CSV file.

```bash
 python designed_goods_movement_routes.py \
  --input ../downloaders/data/designed_goods_movement_routes/truck_routes.csv \
  --output ../processors/processed_data/designed_goods_movement_routes/truck_routes_with_location.csv
```

#### Environment Dataset
This script joins the Heat Vulnerability Index with Zipcode Geometries. The output is a flat CSV file with geometry location details.

```bash
python -m code.processors.merge_hvi_zipcode_geom \
  --hvi   data/environment/heat_vulnerability.csv \
  --zipcode data/environment/zipcode_geom.csv \
  --out   processed_data/environment/hvi_vulnerability_with_geom.csv
```

#### Fixed Obstructions Dataset
This script processes the raw datasets for signposts, utility poles and sidewalks, merging them into a unified dataset.

```bash
python code/processors/fixed_obstructions.py \
  --sidewalks ../downloaders/data/fixed_obstructions/sidewalk_planimetric.csv \
  --telecom_poles ../downloaders/data/fixed_obstructions/telecom_franchise_poles.csv \
  --street_signs ../downloaders/data/fixed_obstructions/street_sign_work_orders.csv \
  --output ../processors/processed_data/fixed_obstructions/sidewalks_with_obstructions.csv
```

#### Bicycle Facilities
No postprocessing script is needed, as the original datasets are being preserved without any merging.

#### Tree Cover and Landscaping Dataset
The script merges Natural Turf Maintenance data with NYC Park Zones to identify landscaped park areas.

```bash
python code/processors/tree_cover_landscaping.py \
  --turf_maintenance ../downloaders/data/tree_cover_landscaping/natural_turf_maintenance.csv \
  --parks_zones ../downloaders/data/tree_cover_landscaping/parks_zones.csv \
  --output ../processors/processed_data/tree_cover_landscaping/parks_with_landscaping.csv
```

#### Transit Stops and Routes 
No postprocessing script is needed, as the original datasets are being preserved without any merging.

#### Curb Infrastructure: Sidewalks, crosswalks, driveways, curb ramps, medians, refuges, curb extensions
This script integrates sidewalk geometries with nearby features such as pedestrian ramps, raised crosswalks, and medians using spatial joins.

```bash
python curb_infrastructure.py \
  --sidewalks data/curb_infrastructure/sidewalks.csv \
  --pedestrian_ramps data/curb_infrastructure/pedestrian_ramps.csv \
  --raised_crosswalks data/curb_infrastructure/raised_crosswalks.csv \
  --medians data/curb_infrastructure/medians.csv \
  --output processed_data/sidewalks_with_curb_features.csv
```

#### Rail Routes and Crossings Dataset
This script downloads and merges railroad line geometries with nearby or intersecting rail crossing points.

```bash
python code/processors/rail_routes_and_crossings.py \
  --railroads ../downloaders/data/rail_routes_and_crossings/railroad_lines.csv \
  --crossings ../downloaders/data/rail_routes_and_crossings/rail_crossings_nyc.csv \
  --output ../processors/processed_data/rail_routes_and_crossings_combined.csv
```

#### Injuries
No postprocessing script is needed, as the original datasets are being preserved without any merging.

#### Urban Design/Frontage
No postprocessing script is needed, as the original datasets are being preserved without any merging.

#### Multi Use Paths and Public Open Spaces Dataset
This script processes open space polygons, open streets, and street centerlines data:

```bash
python code/processors/public_open_spaces.py  \
  --open_spaces ../downloaders/data/public_open_spaces/open_spaces.csv \
  --open_streets ../downloaders/data/public_open_spaces/open_streets.csv \
  --centerlines ../downloaders/data/public_open_spaces/centerline.csv \
  --output ../processors/processed_data/public_open_spaces_final.csv
```

#### Land Use Dataset
This script processes the raw datasets for public facilities, licensed businesses, and sidewalks, merging them into a spatially enriched dataset. Facilities and licenses are spatially joined to sidewalk geometries to provide proximity-based land use context.

```bash
python code/processors/land_use.py \
  --sidewalks ../downloaders/data/land_use/sidewalks.csv \
  --facilities ../downloaders/data/land_use/facilities.csv \
  --licenses ../downloaders/data/land_use/licenses.csv \
  --output ../processors/processed_data/land_use/sidewalks_with_land_use.csv
```

#### Transit Ridership
No postprocessing script is needed, as the original datasets are being preserved without any merging.

#### Social Determinants of Health Dataset
No postprocessing script is needed, as the original datasets are being preserved without any merging.


### Other Datasets
To be added as needed.

## Contributing

To add a new processor:

1. Add a `Python` script in [code/processors](./) to clean, transform, or reformat the dataset.
   - If multiple scripts are needed for one dataset, organize them in a subdirectory named after the dataset ID or source (e.g., `code/processors/your_dataset_id/`).
2. Add CLI usage instructions and a brief description of the processing to this `README.md`.

---
