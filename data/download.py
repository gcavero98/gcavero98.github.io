import os
from pathlib import Path

months = ['Gener', 'Febrer', 'Marc', 'Abril', 'Maig', 'Juny', 'Juliol', 'Agost', 'Setembre', 'Octubre', 'Novembre',
          'Desembre']
base_url = "https://opendata-ajuntament.barcelona.cat/resources/bcn/BicingBCN"
download_folder = Path('./')

for year in [2022, 2021, 2020, 2019]:
    print(f"{year=}")
    year_folder = download_folder / str(year)
    year_folder.mkdir(parents=True, exist_ok=True)

    for month, month_name in zip(range(1, 12 + 1), months):
        print(f"{year} - {month}")
        url = f"{base_url}/{year}_{month:02d}_{month_name}_BicingNou_ESTACIONS.7z"

        month_folder = year_folder / str(month)
        month_folder.mkdir(parents=True, exist_ok=True)
        fname = month_folder / "data.csv"

        # os.system(f"curl '{url}' --output '{fname}'")
        # os.system(f"7z x '{fname}'")
        # os.system(f"rm '{year}_{month:02d}_{month_name}_BicingNou_ESTACIONS.7z'")
