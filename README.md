# Input Data Files

## Overview

This branch contains the input datasets required to execute the scripts available in the main branch of the repository.

The files in this branch are used for calculating ALR values, estimating wetland performance, and evaluating the costs associated with the proposed wetland areas.

## Files

| File                                   | Description                                                                                                                   |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `Flöde_202601010245.xlsx`              | Flow measurements provided by Ekeby Wetland.                                                                                  |
| `Reningsgrad, Ptot, BOD och Ntot.xlsx` | Water quality and purification data from Ekeby Wetland.                                                                       |
| `Degree_of_purification.xlsx`          | Processed version of the purification dataset used in the area analysis.                                                      |
| `Calculated_costs.xlsx`                | Cost estimates for the analyzed wetland areas. This file must be updated if new candidate areas are included in the analysis. |

## Data Origin

The original flow and purification datasets were measured and provided by Ekeby Wetland.

The remaining datasets were derived and processed by the authors for use in the analyses presented in the bachelor's thesis.

## Usage

These files are used by the scripts located in the main branch:

* `calculation_of_ekeby_alr_value.py`
* `calculation_of_area.py`

The datasets should be kept in their original format to ensure compatibility with the scripts.

## Authors

The processing of these datasets and their integration into the analysis were carried out by the authors of the bachelor's thesis.


## Repository Structure

```text
.
├── README.md
├── Flöde_202601010245.xlsx
├── Reningsgrad, Ptot, BOD och Ntot.xlsx
├── Degree_of_purification.xlsx
└── Calculated_costs.xlsx
```
