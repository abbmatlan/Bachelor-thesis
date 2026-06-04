# Identification and Dimensioning of Wetlands for Reduced Eutrophication

## Overview

This repository contains all code and data used in the bachelor's thesis *"Identifiering och dimensionering av våtmarker för minskad övergödning"*.

All code was developed exclusively by the authors and forms a significant part of the analyses and results presented in the thesis.

The repository contains two Python scripts that constitute the core of the computational work.

## Files

| File                                | Description                                                                                              |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `Calculation_Of_EKEBY_ALR_Value.py` | Calculates the ALR (Areal Loading Rate) value used throughout the study.                                 |
| `Calculation_Of_Area.py`            | Main script used for wetland sizing and evaluation based on ALR values and simulated area-specific data. |

## Data Sources

The script `Calculation_Of_EKEBY_ALR_Value.py` uses the following input files:

* `Reningsgrad, Ptot, BOD och Ntot.xlsx`
* `Flöde_202601010245.xlsx`

These datasets were measured and provided by Ekeby Wetland.

The script calculates an ALR value that serves as a key parameter in the thesis.

## Wetland Area Analysis

The script `Calculation_Of_Area.py` is the primary script used in the study. It utilizes the ALR value calculated by `Calculation_Of_EKEBY_ALR_Value.py` together with datasets containing simulated flow rates and nutrient concentrations for the candidate wetland areas identified through the GIS analysis.

Data describing each individual wetland area can be found in the branch:

```text
DATA_For_Wetland_Areas
```

within this repository.

## Repository Structure

```text
.
├── README.md
├── Calculation_Of_EKEBY_ALR_Value.py
└── Calculation_Of_Area.py
```

## Authors

All code and analyses contained in this repository were developed by the authors of the bachelor's thesis.

