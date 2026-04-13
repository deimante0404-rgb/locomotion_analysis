"""
Lokomotorinio aktyvumo analizė, skirtingų vaisto dozių palyginimas. Tikslas: vizualizuoti kaip skirtingos vaisto dozės 
veikia gyvūno lokomototinį aktyvumą.
1.Eksperimento metu duomenys apie gyvūno judėjimą rinkti naudojant infraraudonųjų spindulių sensorius.
Šie duomenys - failo IRS kanale, nuskaitomi šio kanalo duomenys iš kiekvieno gyvūno. 
2.Lokomotorinis aktyvumas stebėtas keturias valandas po dozės suleidimo, vieno trial trukmė - 6 sekundės.
Signalas skaidomas į 6s langus ir apskaičiuojama kiekvieno lango vidutinė vertė.
3.Braižoma sklaidos diagrama kuriame palygnami grupių vidurkiai.
"""

import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from config import SAMPLING_RATE, WINDOW_DURATION, GROUP_SIZE, GROUPS, COLORS
WINDOW_LEN = int(WINDOW_DURATION * SAMPLING_RATE)
#Iš kiekvieno failo nuskaitomas IRS kanalas ir signalas grąžinamas kaip numpy masyvąs, 
# jei faile IRS kanalo nėra ar failas netinkamas, grąžina none.
def load_irs_signal(filepath):
    header = pd.read_csv(filepath, sep='\t', nrows=0)
    cols = header.columns.astype(str).str.replace('"', '').str.strip()
    irs_cols = [c for c in cols if re.match(r'^IRS\d+$', c)]
    if not irs_cols:
        return None
    df = pd.read_csv(filepath, sep='\t', usecols=irs_cols)
    df.columns = [str(c).replace('"', '').strip() for c in df.columns]
    for col in df.columns:
        values = pd.to_numeric(df[col], errors='coerce').to_numpy()
        if np.nanmean(values) > 0.1:
            return values

    return None

#Iš IRS signalo apskaičiuojamos judėjimo reikšmės, kiekvienas taškas atspindi vidutinį aktyvumą per 6s laiko tarpą (vienas trial)
def compute_motion(signal):
    signal = signal[~np.isnan(signal)]
    if len(signal) < WINDOW_LEN:
        return None
    usable_len = (len(signal) // WINDOW_LEN) * WINDOW_LEN
    signal = signal[:usable_len]
    motion = signal.reshape(-1, WINDOW_LEN).mean(axis=1)
    return motion

#apdorojami visi .txt failai esantys direktorijoje ir apskaičiuojamas visos grupės vidutinis lokomotorinis aktyvumas
def get_group_mean_motion(folder):
    all_motion = []
    processed_files = []

    txt_files = sorted(f for f in os.listdir(folder) if f.endswith(".txt"))

    for filename in txt_files:
        filepath = os.path.join(folder, filename)
        try:
            signal = load_irs_signal(filepath)

            if signal is None:
                print(f"  [{filename}] nėra IRS stulpelio")
                continue

            motion = compute_motion(signal)

            if motion is None:
                print(f"  [{filename}] per trumpas signalas")
                continue

            all_motion.append(motion)
            processed_files.append(filename)

        except Exception as e:
            print(f"  [{filename}] klaida: {e}")

    if not all_motion:
        raise ValueError(f"Nepavyko apdoroti nei vieno failo iš: {folder}")

    #Sulyginama pagal trumpiausią įrašą
    min_len = min(len(x) for x in all_motion)
    arr = np.array([x[:min_len] for x in all_motion])

    #Visų grupės gyvūnų vidurkis
    mean_motion = arr.mean(axis=0)

    #Retinimas: 1 taškas: GROUP_SIZE*6s=60s
    usable_len = (len(mean_motion) // GROUP_SIZE) * GROUP_SIZE
    mean_motion = mean_motion[:usable_len]
    mean_motion_reduced = mean_motion.reshape(-1, GROUP_SIZE).mean(axis=1)

    return mean_motion_reduced, processed_files


def plot_locomotion(results, global_min_len):
    time_minutes = (
        np.arange(global_min_len) * GROUP_SIZE * WINDOW_DURATION / 60
    )

    plt.figure(figsize=(12, 5))
    for group_name, motion in results.items():
        plt.scatter(
            time_minutes,
            motion[:global_min_len],
            s=25,
            color=COLORS[group_name],
            edgecolors='none',
            label=group_name,
        )

    plt.title("Lokomotorinio aktyvumo palyginimas tarp ketamino dozių")
    plt.xlabel("Laikas (min)")
    plt.ylabel("Aktyvumo trukmė per sekundę (vidutinė reikšmė)")
    plt.ylim(0, 4)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("locomotion_comparison.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("Grafikas išsaugotas: locomotion_comparison.png")


if __name__ == "__main__":
    results = {}

    for group_name, folder in GROUPS.items():
        print(f"\nApdoroju: {group_name}")
        motion, files = get_group_mean_motion(folder)
        results[group_name] = motion
        print(f"  Failų: {len(files)}, taškų: {len(motion)}")

    global_min_len = min(len(m) for m in results.values())
    plot_locomotion(results, global_min_len)