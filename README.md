# Identification and Dimensioning of Wetlands for Reduced Eutrophication in Stockholm, Sweden

## Overview

This repository contains all code and data used in the bachelor's thesis *"Identifiering och dimensionering av våtmarker för minskad övergödning"*.

All code was developed exclusively by the authors and constitutes a significant part of the analyses and results presented in the thesis.

The repository contains two Python scripts that form the core of the computational work.

## Files

| File                                | Description                                                                                              |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `calculation_of_ekeby_alr_value.py` | Calculates the ALR (Areal Loading Rate) value used throughout the study.                                 |
| `calculation_of_area.py`            | Main script used for wetland sizing and evaluation based on ALR values and simulated area-specific data. |

## Data Sources

The script `calculation_of_ekeby_alr_value.py` uses the following input files:

* `Reningsgrad, Ptot, BOD och Ntot.xlsx`
* `Flöde_202601010245.xlsx`

These datasets were measured and provided by Ekeby Wetland and can be found in the following branch:

```text
input-data
```

The script calculates an ALR value that serves as a key parameter throughout the thesis.

## Wetland Area Analysis

The script `calculation_of_area.py` is the primary script used in the study. It utilizes the ALR value calculated by `calculation_of_ekeby_alr_value.py` together with datasets containing simulated flow rates and nutrient concentrations for the candidate wetland areas identified through the GIS analysis.

Data describing each individual wetland area can be found in the following branch:

```text
wetland-area-data
```

The script also uses two additional input files:

* `Degree_of_purification.xlsx`
* `Reningsgrad, Ptot, BOD och Ntot.xlsx`

The first dataset is a reworked version of `Reningsgrad, Ptot, BOD och Ntot.xlsx`. The second dataset was created by calculating the costs of the analyzed areas. This file must be updated if new areas are selected for analysis.

Both datasets can be found in the following branch:

```text
input-data
```

## Repository Organization

The repository is organized into three branches:

```text
main
├── Python scripts
└── Main README

input-data
├── Flöde_202601010245.xlsx
├── Reningsgrad, Ptot, BOD och Ntot.xlsx
├── Degree_of_purification.xlsx
└── Calculated_costs.xlsx

wetland-area-data
├── 7048_Monthly_values.xlsx
├── 7048_Volumetric_flow.xlsx
├── 7133_Monthly_values.xlsx
├── 7133_Volumetric_flow.xlsx
└── ...
```

* **main** contains all Python code used in the analyses.
* **input-data** contains datasets required as inputs to the scripts.
* **wetland-area-data** contains the simulated datasets for the candidate wetland areas identified through the GIS analysis.


## Authors

All code and analyses contained in this repository were developed by the authors of the bachelor's thesis.
