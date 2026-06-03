# -*- coding: utf-8 -*-
"""
Last updated on Wed Jun  3 18:35:12 2026

@author: Mathias Landström & Karl Norlander
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --------------------
# DATA
# --------------------
concentrations = pd.read_excel('Reningsgrad, Ptot, BOD och Ntot.xlsx', header=None)
flows = pd.read_excel('Flöde_202601010245.xlsx')

# --------------------
# DATA PROCESSING
# --------------------
ha = concentrations.iloc[:, 6:]
P_out = ha.iloc[0]
P_removal_efficiency = ha.iloc[1]
N_out = ha.iloc[2]  # unit: C = [mg/L]
N_removal_efficiency = ha.iloc[3]

fl = flows.iloc[5:-4]  # direct trimming
Date = fl.iloc[:, 1].astype(str)
Q = fl.iloc[:, 5]  # flow rate [m3/day]

# --------------------
# REMOVAL EFFICIENCY
# --------------------
print("Average removal efficiency:", round(np.mean(N_removal_efficiency), 2), "%")

# --------------------
# FUNCTION: MONTHLY CONCENTRATION
# --------------------
def calc_monthly_concentration(N_out, N_removal_efficiency):
    # Converts effluent concentration and % removal efficiency
    # to influent concentration.
    return N_out / (0.01 * (100 - N_removal_efficiency))

C_N_month = calc_monthly_concentration(
    N_out,
    N_removal_efficiency
).values

# --------------------
# MONTH MAPPING
# --------------------
months = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
    "may": 5, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "oct": 10, "nov": 11, "dec": 12
}

# Create month index for each row
def extract_month_index(date_series):
    month_idx = []
    current_month = 0

    for d in date_series:
        for name, num in months.items():
            if name in d:
                current_month = num
                break

        month_idx.append(current_month - 1)  # index 0–11

    return np.array(month_idx)

month_idx = extract_month_index(Date)

# --------------------
# CALCULATE ALR
# --------------------
area = 27 * 100 * 100  # [m2] Area of Ekeby

ALR = (
    Q.values *
    (1 / (24 * 3600)) *
    C_N_month[month_idx]
) / area  # [kg/(day*m2)]

# --------------------
# PLOTTING FUNCTION
# --------------------
def scatter_plot(x, y, xlabel, ylabel, title=None):
    plt.scatter(x, y)
    plt.axhline(0, linewidth=1)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if title:
        plt.title(title)

    plt.show()

# --------------------
# INITIAL PLOT
# --------------------
scatter_plot(Q, ALR, "Q [m3/day]", "ALR [kg/(d*m2)]")

# --------------------
# IQR FILTER FUNCTION
# --------------------
def iqr_filter(x, y):
    q1, q3 = np.quantile(y, [0.25, 0.75])
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    mask = (y >= lower) & (y <= upper)

    return x[mask], y[mask], lower, upper

# Filter outliers
x_f, y_f, low, high = iqr_filter(Q.values, ALR)

scatter_plot(
    x_f,
    y_f,
    "Q [m3/day]",
    "ALR [kg/(d*m2)]",
    "Filtered values"
)

# Percentage removed
print(
    "\nAmount of removed ALR outliers:",
    round((1 - len(y_f) / len(ALR)) * 100, 2),
    "%"
)

# --------------------
# QUARTILES
# --------------------
q50 = np.quantile(y_f, 0.5)
q25 = np.quantile(y_f, 0.25)

mask_q50 = y_f < q50
mask_q25 = y_f < q25

x_q50, y_q50 = x_f[mask_q50], y_f[mask_q50]
x_q25, y_q25 = x_f[mask_q25], y_f[mask_q25]

# --------------------
# AVERAGES
# --------------------
# print("ALR_mean:", np.mean(y_f))

print("ALR_mean_q50, lower half:", np.mean(y_q50))
print("ALR_mean_q25, lower 25%:", np.mean(y_q25))
print("REFERENCE: ALR_mean:", np.mean(y_f))

# --------------------
# Ekeby Wetland (Hydraulic Retention Time)
# --------------------
# Conversion factor for Ekeby wetland

q1, q3 = np.quantile(Q, [0.25, 0.75])
iqr = q3 - q1

lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

filtered_Q_Ekeby = Q[(Q > lower) & (Q < upper)]

# Split into quantiles
Q_q50_Ekeby_limit = np.quantile(filtered_Q_Ekeby, 0.5)

Q_q50_Ekeby = filtered_Q_Ekeby[
    filtered_Q_Ekeby > Q_q50_Ekeby_limit
]

print(
    "Amount of removed Q_Ekeby outliers:",
    round(
        (len(Q) - len(filtered_Q_Ekeby)) /
        len(Q) * 100,
        2
    ),
    "%"
)

# --------------------
# Actual retention time for Ekeby wetland
# when epsilon = 1 and without "smart design"
# --------------------
h_avg = 1

A_Ekeby = 27 * 100 * 100  # [m2]

t_Ekeby = (
    h_avg * A_Ekeby /
    (np.mean(Q_q50_Ekeby) / 24)
)  # [m] * [m2] / [m3/h]

print(
    "Retention time in the scaled-down Ekeby model:",
    round(t_Ekeby, 1),
    "h"
)

print(
    "Retention time in the real Ekeby wetland ~",
    round(6 * 24),
    "h"
)

print(
    "Scaling factor for Ekeby:",
    round((6 * 24) / t_Ekeby,5)
)

