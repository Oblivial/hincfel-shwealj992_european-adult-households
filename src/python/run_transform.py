import pandas as pd

from pathlib import Path
from transforms import shweal_by_country_year  


wid_folder = Path("../../data/raw/wid_all_data_2002_2024_europe")
ess_folder = Path("../../data/raw/ess-Datafile-subset-socio-all-runs-all-countries")

target_folder = Path("../../data/processed")

def main():
    
    # Process WID Data
    print(f"WID folder path: {wid_folder.resolve()}")
    print(f"WID folder exists: {wid_folder.exists()}")
    
    dataframe_wid_target = pd.DataFrame()
    
    # Iterate through all countries' CSV files in the WID folder
    csv_files = list(wid_folder.glob("*.csv"))
    print(f"Found {len(csv_files)} CSV files")
    
    for csv_file in csv_files:
        if "-" not in csv_file.stem:  # Only countries no regions
            df = pd.read_csv(csv_file, sep=";")
            # Concat current country's data to the target DataFrame
            dataframe_wid_target = pd.concat([dataframe_wid_target, 
                                              shweal_by_country_year(df)])
        else:
            print("No countries found, check folder structure and file names.")
    
    # Save the resulting DataFrame to a CSV file
    dataframe_wid_target.to_csv(Path(target_folder / "shweal_by_country_year.csv"), index=False)
  
    # Process ESS Data
    dataframe_ess_target = pd.DataFrame()
    
            
main()