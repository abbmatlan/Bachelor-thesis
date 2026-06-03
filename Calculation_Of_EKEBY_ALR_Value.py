import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --------------------
#  DATA
# --------------------
halter = pd.read_excel('Reningsgrad, Ptot, BOD och Ntot.xlsx', header=None)
flöden = pd.read_excel('Flöde_202601010245.xlsx')

# --------------------
# DATAHANTERING
# --------------------
ha = halter.iloc[:, 6:]
P_ut = ha.iloc[0]
Reningsgrad_P = ha.iloc[1]
N_ut = ha.iloc[2] # enhet: C = [mg/l]
Reningsgrad_N = ha.iloc[3]
fl = flöden.iloc[5:-4]  # direkt trimning
Datum = fl.iloc[:, 1].astype(str)
Q = fl.iloc[:, 5]  # flöde [m3/dag]

# --------------------
# RENINGSHALT
# --------------------
print("medelvärde på reningshalt:",round(np.mean(Reningsgrad_N),2),"%")

# --------------------
# FUNKTION: MONTHLY CONCENTRATION
# --------------------
def calc_monthly_concentration(N_ut, Reningsgrad_N):
    return N_ut / (0.01 * (100 - Reningsgrad_N)) # omvandlar utgående halt och %-rening till ingående halt,
                                                # alltså koncentration. delar mg/l på 
C_N_månad = calc_monthly_concentration(N_ut, Reningsgrad_N).values

# --------------------
# MAPPNING AV MÅNAD
# --------------------
månader = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
    "maj": 5, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "okt": 10, "nov": 11, "dec": 12
}

# skapa månad per rad
def extract_month_index(datum_series):
    month_idx = []
    current_month = 0
    for d in datum_series:
        for name, num in månader.items():
            if name in d:
                current_month = num
                break
        month_idx.append(current_month - 1)  # index 0–11
    return np.array(month_idx)
month_idx = extract_month_index(Datum)


# --------------------
# BERÄKNAR ALR
# --------------------
yta = 27 * 100 * 100 # [m2] AREA på Ekeby
ALR = (Q.values * (1 / (24 * 3600)) * C_N_månad[month_idx]) / yta # [kg/(dag*m2)]

# --------------------
# PLOT FUNKTION
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
scatter_plot(Q, ALR, "Q [m3/dag]", "ALR [kg/(d*m2)]")

# --------------------
# IQR FILRTRERINGSFUNKTION
# --------------------
def iqr_filter(x, y):
    q1, q3 = np.quantile(y, [0.25, 0.75])
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    mask = (y >= lower) & (y <= upper)
    return x[mask], y[mask], lower, upper

# filtrera
x_f, y_f, low, high = iqr_filter(Q.values, ALR)
scatter_plot(x_f, y_f, "Q [m3/dag]", "ALR [kg/(d*m2)]", "Filtrerade värden")
# % borttagna
print("\nAmount of removed outliers of ALR:",round((1 - len(y_f)/len(ALR)) * 100,2), "%")


# --------------------
# KVARTILER
# --------------------
q50 = np.quantile(y_f, 0.5)
q25 = np.quantile(y_f, 0.25)

mask_q50 = y_f < q50
mask_q25 = y_f < q25

x_q50, y_q50 = x_f[mask_q50], y_f[mask_q50]
x_q25, y_q25 = x_f[mask_q25], y_f[mask_q25]


# --------------------
# MEDELVÄRDEN
# --------------------
#print("ALR_medel:", np.mean(y_f))
print("ALR_medel_q50, undre halvan:", np.mean(y_q50))
print("ALR_medel_q25, undre 25%", np.mean(y_q25))
print("REFERENS: ALR_medel", np.mean(y_f))


# --------------------
# Ekeby våtmark (Uppbehållstid)
# --------------------
# Konverteringsfaktor för Ekeby våtmark

q1, q3 = np.quantile(Q, [0.25, 0.75])
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr
filtered_Q_Ekeby = Q[(Q > lower) & (Q < upper)]

#delar upp i kvantiler
Q_q50_Ekeby_limit = np.quantile(filtered_Q_Ekeby, 0.5)
Q_q50_Ekeby = filtered_Q_Ekeby[filtered_Q_Ekeby > Q_q50_Ekeby_limit] # m3/s

print("Amount of removed outliers of Q_Ekeby",round((len(Q)-len(filtered_Q_Ekeby))/len(Q)*100, 2), "%")


# --------------------
# Actual Residual time for Ekeby wetlan WHEN epsilon=1 & WITHOUT "smart design"
# --------------------
h_avg=1
A_Ekeby = 27 * 100 * 100 # [m2]
t_Ekeby = h_avg*A_Ekeby/((np.mean(Q_q50_Ekeby)/24)) #[m]*[m2]/[m3/h]
print("Antal timmar Ekeby har i upphållstid med en nerskalad modell",round(t_Ekeby,1),"h")
print("Antal timmar Ekeby har i upphållstid i verkligheten ~",round(6*24),"h")
print("skalningsfaktor Ekeby:",(6*24)/t_Ekeby)

