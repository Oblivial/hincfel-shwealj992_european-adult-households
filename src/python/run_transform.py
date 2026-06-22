import pandas as pd

from pathlib import Path
from transforms import stfeco_by_country_year, shweal_by_country_year
from util import getESSFolderPath, getOutputFolderPath, getWIDFolderPath

def main():
    
    wid_folder = Path(getWIDFolderPath())
    ess_folder = Path(getESSFolderPath())

    target_folder = Path(getOutputFolderPath())
    
    # Process WID Data
    print(f"WID folder path: {wid_folder.resolve()}")
    
    dataframe_wid_target = pd.DataFrame()
    # Iterate through all countries' CSV files in the WID folder
    csv_files = list(wid_folder.glob("*.csv"))
    print(f"Found {len(csv_files)} CSV files")
    
    for csv_file in csv_files:
        csv_filename = csv_file.stem
        if "-" not in csv_filename and "countries" not in csv_filename and "metadata" not in csv_filename:  # Only countries no regions, no countries list, no metadata
            print(f"Processing file: {csv_filename}")
            df = pd.read_csv(csv_file, sep=";")
            if df.empty:
                print(f"Warning: The file {csv_filename} is empty. Skipping.")
            else:
                # Concat current country's data to the target DataFrame
                dataframe_wid_target = pd.concat([dataframe_wid_target, 
                                              shweal_by_country_year(df)])
        else:
            print(f"Skipping file: {csv_filename}")
    
    # Save the resulting DataFrame to a CSV file
    dataframe_wid_target.to_csv(Path(target_folder / "shweal_by_country_year.csv"), index=False)
  
    # Process ESS Data
    dataframe_ess_target = pd.DataFrame()
    print(f"ESS folder path: {ess_folder.resolve()}")
    dataframe_ess_target = stfeco_by_country_year(pd.read_csv(ess_folder / "Datafile-subset.csv"))
    dataframe_ess_target.to_csv(Path(target_folder / "stfeco_by_country_year.csv"), index=False)
    
    
    print ("Done!")
            
main()