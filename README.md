# Wetland Area Data

## Overview

This branch contains the simulated datasets for all candidate wetland areas identified through the GIS analysis conducted in the bachelor's thesis.

For each area, two datasets are provided:

* Monthly nutrient and flow statistics (`Monthly_values`)
* Simulated volumetric flow data (`Volumetric_flow`)

These datasets are used by `calculation_of_area.py` in the main branch to estimate required wetland size, purification performance, and cost-effectiveness.

## File Structure

Each wetland area is identified by a unique area ID.

Example:

| File                        | Description                                                           |
| --------------------------- | --------------------------------------------------------------------- |
| `7133_Monthly_values.xlsx`  | Monthly simulated values for area 7133.                               |
| `7133_Volumetric_flow.xlsx` | Simulated volumetric flow data for area 7133.                         |
| `7585_Monthly_values.xlsx`  | Monthly simulated values for area 7585.                               |
| `7585_Volumetric_flow.xlsx` | Simulated volumetric flow data for area 7585.                         |
| ...                         | Additional candidate wetland areas follow the same naming convention. |

## Data Origin

The datasets contained in this branch originate from model outputs generated using SMHI's S-HYPE hydrological model.

The data were downloaded from SMHI Vattenwebb's "Model Data per Area" service:

https://vattenwebb.smhi.se/modelarea/

S-HYPE (Swedish Hydrological Predictions for the Environment) is a hydrological model developed by SMHI and used to simulate water flow and nutrient transport within Swedish catchment areas. The model provides estimates of water quantity and water quality variables for individual sub-catchment areas throughout Sweden.

For each candidate wetland area, monthly nutrient transport data and volumetric flow data were downloaded and processed for use in the wetland sizing analysis presented in the bachelor's thesis. The datasets included in this branch are therefore derived from S-HYPE model outputs rather than direct field measurements.

## Naming Convention

Files follow the structure:

```text
[Area_ID]_Monthly_values.xlsx
[Area_ID]_Volumetric_flow.xlsx
```

where:

* `Area_ID` is the unique identifier assigned to the candidate wetland area.
* `Monthly_values` contains monthly aggregated data.
* `Volumetric_flow` contains simulated flow data used in the sizing calculations.

## Usage

The datasets in this branch serve as input to:

```text
calculation_of_area.py
```

located in the main branch of the repository.

## Repository Structure

```text
.
├── README.md
├── 7048_Monthly_values.xlsx
├── 7048_Volumetric_flow.xlsx
├── 7133_Monthly_values.xlsx
├── 7133_Volumetric_flow.xlsx
├── 7585_Monthly_values.xlsx
├── 7585_Volumetric_flow.xlsx
├── 7772_Monthly_values.xlsx
├── 7772_Volumetric_flow.xlsx
└── ...
```

## Authors

The datasets were generated and processed by the authors of the bachelor's thesis for use in the wetland sizing and evaluation analyses.
