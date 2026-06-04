# Identification and Dimensioning of Wetlands for Reduced Eutrophication

## Overview

This repository contains all code and data used in the bachelor's thesis *"Identifiering och dimensionering av våtmarker för minskad övergödning"*.

All code was developed exclusively by the authors and forms a significant part of the analyses and results presented in the thesis.

The repository contains two Python scripts that constitute the core of the computational work.

## Files

| File                                | Description                                                                                              |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `calculation_of_ekeby_alr_value.py` | Calculates the ALR (Areal Loading Rate) value used throughout the study.                                 |
| `calculation_of_area.py`            | Main script used for wetland sizing and evaluation based on ALR values and simulated area-specific data. |

## Data Sources

The script `calculation_of_ekeby_alr_value.py` uses the following input files:

* `Reningsgrad, Ptot, BOD och Ntot.xlsx`
* `Flöde_202601010245.xlsx`

These datasets were measured and provided by Ekeby Wetland.

The script calculates an ALR value that serves as a key parameter in the thesis.

## Wetland Area Analysis

The script `calculation_of_area.py` is the primary script used in the study. It utilizes the ALR value calculated by `calculation_of_ekeby_alr_value.py` together with datasets containing simulated flow rates and nutrient concentrations for the candidate wetland areas identified through the GIS analysis.

Data describing each individual wetland area can be found in the branch:

```text
DATA_For_Wetland_Areas
```
within this repository.

The script also uses two other input files:
* `Degree_of_purification.xlsx`
* `Reningsgrad, Ptot, BOD och Ntot.xlsx`

The first daset is a rework of `Reningsgrad, Ptot, BOD och Ntot.xlsx`. And the last dataset was created by calculating the cost of the analyzed areas. (The last file needs to be changed if new areas a chosen) 

## Repository Structure

```text
.
├── README.md
├── calculation_of_ekeby_alr_value.py
└── calculation_of_area.py
```

## Authors

All code and analyses contained in this repository were developed by the authors of the bachelor's thesis.

