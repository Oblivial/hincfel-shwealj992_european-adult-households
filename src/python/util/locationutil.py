import pandas as pd

from .config import getESSFolderPath, getWIDFolderPath

global countriesLoaded
global countryMappingWID
global countryShortMappingESS
global filteredCountryMapping # Only European countries that are in both datasets

def loadCountryCodes():
    """
    Load country codes and names from a CSV file.
    Compare country codes between ESS and WID datasets and report the differences.
    """
    
    # Wid Countries
    countryMappingWID = pd.read_csv(getWIDFolderPath() + "/WID_countries.csv")
    
    # Filter to only European countries
    filteredCountryMapping = countryMappingWID[countryMappingWID['region'] == 'Europe']
    
    # ESS Countries
    essDataFile = pd.read_csv(getESSFolderPath() + "/Datafile-subset.csv")
    countryShortMappingESS = essDataFile[['cntry']].drop_duplicates()
    
    # Compare country codes between ESS and WID (European countries only)
    wid_codes = set(filteredCountryMapping['alpha2'].values)
    ess_codes = set(countryShortMappingESS['cntry'].values)
    
    in_wid_not_in_ess = wid_codes - ess_codes
    print(f"European WID countries but NOT in ESS ({len(in_wid_not_in_ess)}): {sorted(in_wid_not_in_ess)}")
    
    # Drop WID countries not in ESS from filteredCountryMapping
    filteredCountryMapping = filteredCountryMapping[~filteredCountryMapping['alpha2'].isin(in_wid_not_in_ess)]
    
    countriesLoaded = True

def getFilteredCountryMapping():
    if not countriesLoaded:
        loadCountryCodes()
    return filteredCountryMapping
