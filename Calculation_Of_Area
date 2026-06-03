#—--------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
"""
@author: Mathias Landström & Karl Norlander
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# --------------------
# AREA CONFIGURATION
# --------------------
# Uncomment the desired area setup

# _____________7133______________
# A1

a1= " (A1) "
a = "7133"
b = 113317         # [kg]
c = 221            # [ha]
d = 25.905         # [km2] Sub-catchment area
e = 298.400        # [km2] Total catchment area


# _____________7585______________
# A2
'''
a1= " (A2) "
a = "7585"
b = 22762          # [kg]
c = 89.3           # [ha]
d = 23.938         # [km2] Sub-catchment area
e = 68.745         # [km2] Total catchment area
'''

# _____________7772______________
# A3 (active case)
'''
a1= " (A3) "
a = "7772"
b = 152010         # [kg]
c = 55.5           # [ha]
d = 1.830          # [km2] Sub-catchment area
e = 435.679        # [km2] Total catchment area
'''
'''
# _____________7048______________ 

a1= " (A4) "
a = "7048"
b = 47443          # [kg]
c = 45.6 + 36.5    # [ha] Area of proposed site
d = 62.627         # [km2] Sub-catchment area
e = 85.225         # [km2] Total catchment area
'''



# --------------------
# LOAD AND CLEAN DATA
# --------------------
rening = pd.read_excel('Degree_of_purification.xlsx')  # treatment efficiency
area = pd.read_excel('Excel_Areas/'+a+'_Monthly_values.xlsx')
vol_flow = pd.read_excel('Excel_Areas/'+a+'_Volumetric_flow.xlsx')  # m3/s
cost = pd.read_excel('Calculated_cost_after_simulation.xlsx')

# Extract nitrogen concentration and flow data
N = pd.to_numeric(area.iloc[:, 9], errors='coerce').dropna()
flow = pd.to_numeric(vol_flow.iloc[6:, 2], errors='coerce').dropna()


# --------------------
# FUNCTIONS
# --------------------

def iqr_filter(data):
    """Remove outliers using the IQR method"""
    q1, q3 = np.quantile(data, [0.25, 0.75])
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    mask = (data > lower) & (data < upper)
    return data[mask], data[~mask]

# Used only to compute the lines in the plot (points are calculated separately)
def calc_area(flow_vals, C):
    """Calculate wetland area from flow and concentration"""
    return [(flow_vals * C) / alr for alr in ALR]

# Plot Q75, Q50 and reference curves
def plot_q75_q50(x_q75, y_q75, x_q50, y_q50, x_REFERENS, y_REFERENS, title, point1=None, point2=None, point3=0):
    plt.figure(figsize=(8,5))

    # Convert to hectares
    y75 = np.array(y_q75[1]) / 10000
    y50 = np.array(y_q50[0]) / 10000
    yREFERENS = np.array(y_REFERENS[2]) / 10000

    # Plot curves
    plt.plot(x_q75, y75, label='Q75')
    plt.plot(x_q50, y50, color='orange', label='Q50')
    plt.plot(x_REFERENS, yREFERENS, color='green', label='REFERENCE')

    # Plot selected points and horizontal guide lines
    for p in [point1, point2, point3]:
        if p is not None:
            x, y = p
            plt.plot(x, y, 'o', color='black', markersize=6)
            plt.axhline(y=y, color='black', linestyle=':', alpha=0.5)

    # Labels and styling
    plt.xlabel("Flow [m³/s]")
    plt.ylabel("Area [ha]")
    plt.title(title)
    plt.legend(frameon=False)
    plt.grid(alpha=0.2)

    # Remove top/right borders
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.show()


def calculate_flows(CF_list, Q_highest, label):
    """
    Calculate nitrogen removal and overflow based on max allowed flow
    """
    outgoing_flow = []

    # Split flows into manageable and exceeding capacity
    manageable_flow = [p for p in CF_list if p[0] <= Q_highest]
    unmanageable_flow = [p for p in CF_list if p[0] > Q_highest]
    
    # Redistribute excess flow
    for data in unmanageable_flow:
        manageable_flow.append([Q_highest, data[1], data[2]])
        outgoing_flow.append([data[0] - Q_highest, data[1], data[2]])
    
    tot_N_wetland = 0
    tot_N_out = 0
    
    # Nitrogen treated vs bypassed
    for data in manageable_flow:
        tot_N_wetland += (data[0]*data[1]*10**(-6)*3600*24)*data[2]
        tot_N_out += (data[0]*data[1]*10**(-6)*3600*24)*(1-data[2])
    
    for data in outgoing_flow:
        tot_N_out += (data[0]*data[1]*10**(-6)*3600*24)

    # Output results
    print(f"\n=== Q_highest = {Q_highest} ===")
    print("\nTotal nitrogen removed:", label, round(tot_N_wetland/15, 2), "kg")
    print("Total nitrogen bypassing:", label, round(tot_N_out/15, 2), "kg")
    print("Total nitrogen per year:", label, round((tot_N_wetland+tot_N_out)/15, 2), "kg")
    print("Total efficiency =", label, round(100*tot_N_wetland/(tot_N_wetland+tot_N_out), 2), "%")

    # Flow statistics
    flow_through = sum([f[0] for f in manageable_flow])
    flow_tot = flow_through + sum([f[0] for f in outgoing_flow])

    print("Share of flow treated by wetland:", label, round(100*flow_through/flow_tot, 2), "%")
    
    return tot_N_wetland, tot_N_out, manageable_flow, unmanageable_flow, outgoing_flow


def extract_xy(data):
    x = np.array([point[0] for point in data])
    y = np.array([point[1] for point in data])
    return x, y


def find_flattening_year(y_values, threshold=0.05): # FIND WHERE THE CURVE FLATTENS
    for i in range(1, len(y_values)):
        change = abs(y_values[i] - y_values[i - 1]) / y_values[i - 1]
        if change < threshold:
            return i + 1
    return None


# --------------------
# NITROGEN ANALYSIS
# --------------------
filtered_N, outliers_N = iqr_filter(N)
print("Removed outliers (N):", round(len(outliers_N)/len(N)*100, 2), "%")

# Quantiles
q75_N = np.quantile(filtered_N, 0.75)
q50_N = np.quantile(filtered_N, 0.5)

Q50_N = filtered_N[filtered_N > q50_N]
Q75_N = filtered_N[filtered_N > q75_N]

# Mean concentrations
N_Q75_mean = np.mean(Q75_N) * 1e-3
N_Q50_mean = np.mean(Q50_N) * 1e-3
N_REF_mean = np.mean(filtered_N) * 1e-3

print("Q75 mean N:", round(N_Q75_mean,2), "[kg/m3]")
print("Q50 mean N:", round(N_Q50_mean,2), "[kg/m3]")
print("Reference mean N:", round(N_REF_mean,2), "[kg/m3]")


# --------------------
# FLOW ANALYSIS
# --------------------
filtered_F, outliers_F = iqr_filter(flow)
print("\nRemoved outliers (flow):", round(len(outliers_F)/len(flow)*100, 2), "%")

q75_Flow_limit = np.quantile(flow, 0.75)
q50_Flow_limit = np.quantile(flow, 0.50)

q75_Flow = filtered_F[filtered_F >= q75_Flow_limit].values
q50_Flow = filtered_F[filtered_F >= q50_Flow_limit].values

# Mean flows
median_flow_Q75 = np.mean(q75_Flow)
median_flow_Q50 = np.mean(q50_Flow)
median_flow_REF = np.mean(filtered_F)

print("\nMean flow Q75:", round(median_flow_Q75,2), "[m^3/s]")
print("Mean flow Q50:", round(median_flow_Q50,2), "[m^3/s]")
print("Mean flow REF:", round(median_flow_REF,2), "[m^3/s]")


# --------------------
# AREA CALCULATION (Eq.1)
# A = Q * C / ALR
# --------------------
ALR = np.array([
    5.158947441973675e-05,  # max
    4.551236345405426e-05,  # min
    6.237099182003662e-05   # reference
])

AREA_Q75 = calc_area(q50_Flow, N_Q75_mean)
AREA_Q50 = calc_area(q50_Flow, N_Q50_mean)
AREA_REFERENS = calc_area(q50_Flow, N_REF_mean)


# --------------------
# MIN/MAX WETLAND AREA
# --------------------
Aw_max = (median_flow_Q75 * N_Q75_mean)/ALR[1]
Aw_min = (median_flow_Q50 * N_Q50_mean)/ALR[0]
Aw_REFERENS = (median_flow_REF * N_REF_mean)/ALR[2]

print("\nMax wetland area:", round(Aw_max/(100*100),2), "[ha]")
print("Min wetland area:", round(Aw_min/(100*100),2), "[ha]")
print("Reference wetland area:", round(Aw_REFERENS/(100*100),2), "[ha]")


# --------------------
# PRE-SEDIMENTATION DESIGN
# --------------------
Vs = 0.00011  # settling velocity (m/s)

A_pre_sed_50 = median_flow_Q50/Vs
A_pre_sed_75 = median_flow_Q75/Vs
A_pre_sed_REF = median_flow_REF/Vs

print("\nPre-sedimentation Q50:",round(A_pre_sed_50/(100*100),2),"[ha]")
print("Pre-sedimentation Q75:",round(A_pre_sed_75/(100*100),2),"[ha]")
print("Pre-sedimentation REF:",round(A_pre_sed_REF/(100*100),2),"[ha]")


# --------------------
# TOTAL AREA
# --------------------
A_tot_min= Aw_min + A_pre_sed_50
A_tot_max = Aw_max + A_pre_sed_75
A_tot_ref = Aw_REFERENS + A_pre_sed_REF

print("\nMax total area:", round(A_tot_max/(100*100),2), "[ha]")
print("Min total area:", round(A_tot_min/(100*100),2), "[ha]")
print("Reference total area:", round(A_tot_ref/(100*100),2), "[ha]")


# --------------------
# RESIDENCE TIME
# t = A*h / Q
# --------------------
A_avg = (Aw_max + Aw_min)/2
h_avg = 1
h_sed_avg = 2

# Sedimentation time
t_sed_exp = h_sed_avg*A_pre_sed_50/(median_flow_Q50*3600*24)
t_sed_min = h_sed_avg*A_pre_sed_75/(median_flow_Q75*3600*24)
t_sed_ref = h_sed_avg*A_pre_sed_REF/(median_flow_REF*3600*24)

# Wetland time
t_expected = h_avg*A_avg/(median_flow_Q50*3600*24)
t_min = h_avg*A_avg/(median_flow_Q75*3600*24)
t_referens = h_avg*Aw_REFERENS/(median_flow_REF*3600*24)

print("\nResidence time (expected):",round((t_sed_exp+t_expected)*24,2),"hours")


# --------------------
# ADJUSTMENT FACTOR
# --------------------
adjustment_factor = 1.2352215944758318

print("Adjusted residence time:", round((t_sed_exp+t_expected)*24*adjustment_factor,2), "hours")


# --------------------
# AREA BASED ON MIN RESIDENCE TIME
# --------------------
if t_expected < 48:
    t_x = 48/adjustment_factor

    A_res_time_q50 = (t_x-t_sed_exp)*3600*(median_flow_Q50/h_avg)
    A_res_time_q75 = (t_x-t_sed_min)*3600*(median_flow_Q75/h_avg)
    A_res_time_ref = (t_x-t_sed_ref)*3600*(median_flow_REF/h_avg)

    A_2_q50 = A_res_time_q50 + A_pre_sed_50
    A_2_q75 = A_res_time_q75 + A_pre_sed_75
    A_2_ref = A_res_time_ref + A_pre_sed_REF

    print("\nArea with 48h residence (Q50):",round(A_2_q50/(100*100),2),"ha")
    print("Area with 48h residence (Q75):",round(A_2_q75/(100*100),2),"ha")
    print("Area with 48h residence (REF):",round(A_2_ref/(100*100),2),"ha")


# --------------------
# PLOT RESULTS
# --------------------
plot_q75_q50(
    q50_Flow, AREA_Q75,
    q50_Flow, AREA_Q50,
    q50_Flow, AREA_REFERENS,
    "Area: "+a+a1,
    [median_flow_Q75, Aw_max/(100*100)],
    [median_flow_Q50, Aw_min/(100*100)],
    [median_flow_REF, Aw_REFERENS/(100*100)]
)


# --------------------
# CATCHMENT SHARE ANALYSIS
# --------------------
print("\nGIS area is", round(100*(c/(d*(100))),2),"% of sub-catchment")
print("GIS area is", round(100*(c/(e*(100))),2),"% of total catchment")


# --------------------
# FLOW-CAPACITY CALCULATIONS
# --------------------
Q_highest_q50 = (A_res_time_q50 + A_pre_sed_50*2)/(48*3600)
Q_highest_q75 = (A_res_time_q75 + A_pre_sed_75*2)/(48*3600)
Q_highest_ref = (A_res_time_ref + A_pre_sed_REF*2)/(48*3600)

print("\nMax flow capacity (Q50):",round(Q_highest_q50,2),"m3/s")
print("Max flow capacity (Q75):",round(Q_highest_q75,2),"m3/s")
print("Max flow capacity (REF):",round(Q_highest_ref,2),"m3/s")


# --------------------
# MERGE FLOW, CONCENTRATION AND TREATMENT DATA
# --------------------

# Daily flow data
vf = vol_flow.iloc[6:].copy()
vf = vf.rename(columns={"Dygnsvärden": "datum", "Unnamed: 2": "flow"})

vf["flow"] = pd.to_numeric(vf["flow"].astype(str).str.replace(",", "."), errors="coerce")
vf["datum"] = pd.to_datetime(vf["datum"], errors="coerce")
vf["år"] = vf["datum"].dt.year
vf["månad"] = vf["datum"].dt.month

# Monthly concentration
conc = area.rename(columns={"Unnamed: 0": "datum", "Total kvävekoncentration [ug/l]": "conc"})

conc["conc"] = pd.to_numeric(conc["conc"].astype(str).str.replace(",", "."), errors="coerce")
conc["datum"] = pd.to_datetime(conc["datum"], errors="coerce")
conc["år"] = conc["datum"].dt.year
conc["månad"] = conc["datum"].dt.month

# Treatment efficiency
renh = rening.copy()
renh["reningshalt"] = pd.to_numeric(renh["reningshalt"].astype(str).str.replace(",", "."), errors="coerce")
renh["datum"] = pd.to_datetime(renh["datum"], errors="coerce")
renh["månad"] = renh["datum"].dt.month

# Merge datasets
result = vf.merge(conc, on=["år", "månad"], how="left")
result = result.merge(renh, on="månad", how="left")

# Final dataset for simulation
CF_list = result[["flow", "conc", "reningshalt"]].values.tolist()


# --------------------
# RUN SIMULATION
# --------------------
calculate_flows(CF_list, Q_highest_q50, "(Q50)")
calculate_flows(CF_list, Q_highest_q75, "(Q75)")
calculate_flows(CF_list, Q_highest_ref, "(REF)")



#------------------------
# GRAPGH SHOWING COST OVER YEAR
# -----------------------
price = []  # Total price in Mkr over a time span of 50 years

'''
[REF,
 Q50,
 Q75]
'''
for _, val in cost.iterrows():
    if str(val["Område"]) == a:
        price.append(val["Total kostnad 50 år [Mkr]"])

# ======================================================
# CREATE DATA
# ======================================================
REF_price = []
Q50_price = []
Q75_price = []
year = 1
while year <= 50:
    REF_price.append([year, price[0] / year])
    Q50_price.append([year, price[1] / year])
    Q75_price.append([year, price[2] / year])
    year += 1

x_ref, y_ref = extract_xy(REF_price)
x_q50, y_q50 = extract_xy(Q50_price)
x_q75, y_q75 = extract_xy(Q75_price)
# ======================================================
# FIND WHERE THE CURVE FLATTENS
# ======================================================
flat_ref = find_flattening_year(y_ref)
flat_q50 = find_flattening_year(y_q50)
flat_q75 = find_flattening_year(y_q75)
# ======================================================
# STYLE # classic matplott colors:
# ======================================================
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(13, 8))
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
blue = colors[0]
orange = colors[1]
green = colors[2]

# ======================================================
# PLOT LINES
# ======================================================
ax.plot(x_ref, y_ref, linewidth=2, label='REF', color=green)
ax.plot(x_q50, y_q50, linewidth=2, label='Q50', color=orange)
ax.plot(x_q75, y_q75, linewidth=2, label='Q75', color=blue)
# ======================================================
# PLOT POINTS
# ======================================================
ax.scatter(x_ref, y_ref, s=35, alpha=0.7)
ax.scatter(x_q50, y_q50, s=35, alpha=0.7)
ax.scatter(x_q75, y_q75, s=35, alpha=0.7)
# ======================================================
# FILL UNDER CURVES
# ======================================================
ax.fill_between(x_ref, y_ref, alpha=0.10)
ax.fill_between(x_q50, y_q50, alpha=0.10)
ax.fill_between(x_q75, y_q75, alpha=0.10)
# ======================================================
# MARK FLATTENING POINT
# ======================================================
ax.axvline(flat_ref, linestyle='--', alpha=0.7)
ax.axvline(flat_q50, linestyle='--', alpha=0.7)
ax.axvline(flat_q75, linestyle='--', alpha=0.7)
# Highlight points
ax.scatter(flat_ref, y_ref[flat_ref - 1], s=120)
ax.scatter(flat_q50, y_q50[flat_q50 - 1], s=120)
ax.scatter(flat_q75, y_q75[flat_q75 - 1], s=120)
# ======================================================
# LABELS
# ======================================================

ax.text(
    flat_ref + 0.5,
    y_ref[flat_ref - 1] + 0.3 * max(y_ref),
    f'REF ~ år {flat_ref}',
    fontsize=11
)

ax.text(
    flat_q50 + 0.5,
    y_q50[flat_q50 - 1] + 0.5 * max(y_ref),
    f'Q50 ~ år {flat_q50}',
    fontsize=11
)

ax.text(
    flat_q75 + 0.5,
    y_q75[flat_q75 - 1] + 0.4 * max(y_ref),
    f'Q75 ~ år {flat_q75}',
    fontsize=11
)
# ======================================================
# TITLE & AXES
# ======================================================
title= 'Område: '+a+a1+', kostnad per år över 50 år' 
ax.set_title(str(title), fontsize=22, pad=20)
ax.set_xlabel('År', fontsize=14)
ax.set_ylabel('Kostnad [Mkr/År]', fontsize=14)
# ======================================================
# GRID & LEGEND
# ======================================================
ax.grid(alpha=0.3)
ax.legend(fontsize=13, frameon=True)
# Remove top/right borders
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# ======================================================
# Y-AXIS
# ======================================================
ax.set_ylim(bottom=0)
# ======================================================
# SHOW PLOT
# ======================================================
plt.tight_layout()
plt.show()


#—---------------------------------------------------------------------------------
