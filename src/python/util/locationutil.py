import pandas as pd

from .config import get_ess_folderpath, get_wid_folderpath

_countries_loaded = False
_country_mapping_wid = None
_country_short_mapping_ess = None
_filtered_country_mapping = None  # Only European countries that are in the WID and the ESS datasets

def load_country_codes():
    """
    Load country codes and names from a CSV file.
    Compare country codes between ESS and WID datasets and report the differences.
    """
    global _countries_loaded
    global _filtered_country_mapping
    global _country_short_mapping_ess
    global _country_mapping_wid
    
    # Wid Countries
    _country_mapping_wid = pd.read_csv(get_wid_folderpath() + "/WID_countries.csv", sep=';')
    
    # Filter to only European countries
    _filtered_country_mapping = _country_mapping_wid[_country_mapping_wid['region'] == 'Europe']
    
    # ESS Countries
    ess_datafile = pd.read_csv(get_ess_folderpath() + "/Datafile-subset.csv")
    _country_short_mapping_ess = ess_datafile[['cntry']].drop_duplicates()
    
    # Compare country codes between ESS and WID (European countries only)
    wid_codes = set(_filtered_country_mapping['alpha2'].values)
    ess_codes = set(_country_short_mapping_ess['cntry'].values)
    
    in_wid_not_in_ess = wid_codes - ess_codes

    # Drop WID countries not in ESS from _filtered_country_mapping
    _filtered_country_mapping = _filtered_country_mapping[~_filtered_country_mapping['alpha2'].isin(in_wid_not_in_ess)]
    
    _countries_loaded = True

def get_countrycodes_not_in_ess():
    """
    Get European country codes that are in WID but not in ESS.
    """
    if not _countries_loaded:
        load_country_codes()
    
    wid_codes = set(_filtered_country_mapping['alpha2'].values)
    ess_codes = set(_country_short_mapping_ess['cntry'].values)
    
    return wid_codes - ess_codes

def get_countrycodes_not_in_wid():
    """
    Get European country codes that are in ESS but not in WID.
    """
    if not _countries_loaded:
        load_country_codes()
    
    wid_codes = set(_filtered_country_mapping['alpha2'].values)
    ess_codes = set(_country_short_mapping_ess['cntry'].values)
    
    return ess_codes - wid_codes    

def get_european_countrycodes():
    """
    Get the list of European country codes (WID filtered by Region, All ESS Countries).
    """
    if not _countries_loaded:
        load_country_codes()
    wid_codes = set(_filtered_country_mapping['alpha2'].values)
    ess_codes = set(_country_short_mapping_ess['cntry'].values)

    # Include all WID European codes and add any ESS codes not already present
    combined = sorted(wid_codes.union(ess_codes))
    return combined

def get_filtered_country_mapping():
    if not _countries_loaded:
        load_country_codes()
    return _filtered_country_mapping
