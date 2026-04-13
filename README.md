# GyvūnųLokomotorinio aktyvumo analizė

Šis kodas skirtas analizuoti gyvūnų (pelių) lokomotorinio aktyvumo duomenis, surinktus eksperimento metu skiriant skirtingas
ketamino injekcijas (10 mg/kg, 20 mg/kg, 40 mg/kg). 

1. Nuskaitomi IRS kanalo duomenys iš kiekvieno gyvūno
2. Signalas suskaidomas į 6s langus
3. Grupių vidurkiai palyginami grafike

Kiekvienas .txt failas - vienas gyvūnas.
Failuose turi būti IRS1, IRS2 arba panašūs stulpeliai, su lokomotorinio aktyvumo duomenimis (šiuo atveju - iš infraraudonųjų spindulių judesio sensorių)

# paleidimas

1. pip install -r requirements.txt

2. Pakeisti failų kelius config.py

3. Paleisti locomotion.py



# Parametrai (config.py)

- SAMPLING_RATE: diskretizavimo dažnis (Hz)
- WINDOW_DURATION: vieno lango trukmė (s)
- GROUP_SIZE: retinimo koeficientas