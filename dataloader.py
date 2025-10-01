import csv
from pathlib import Path
import pandas as pd


def main():
    file_root = Path("./data challenge/data challenge/")
    cliente_file = file_root / "cliente.csv"
    polizze_file = file_root / "polizze.csv"
    preventivi_file = file_root / "preventivi.csv"
    garanzie_file = file_root / "garanzie.csv"

    cliente = pd.read_csv(cliente_file)
    polizze = pd.read_csv(polizze_file)
    preventivi = pd.read_csv(preventivi_file)
    garanzie = pd.read_csv(garanzie_file)

    ...



if __name__ == "__main__":
    main()
