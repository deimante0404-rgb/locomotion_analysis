#Parametrai analizei, pasirinkti deskritizavimo dažnį, vieno trial'o trukmę, retinimą.
SAMPLING_RATE = 2000        #Hz
WINDOW_DURATION = 6.0       
GROUP_SIZE = 10             #Retinimas: 1 taškas = 60s

#Nurodyti grupių failų kelius ir spalvas
GROUPS = {
    "Ketaminas 10 mg/kg": "/Users/deimantemickute/Desktop/Bakalauras/Ket10_ASSR",
    "Ketaminas 20 mg/kg": "/Users/deimantemickute/Desktop/Bakalauras/KET20_ASSR",
    "Ketaminas 40 mg/kg": "/Users/deimantemickute/Desktop/Bakalauras/KET40_ASSR",
}

COLORS = {
    "Ketaminas 10 mg/kg": "#2ca02c",
    "Ketaminas 20 mg/kg": "#1f77b4",
    "Ketaminas 40 mg/kg": "#d62728",
}