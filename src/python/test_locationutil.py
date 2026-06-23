from util import get_filtered_country_mapping
import pandas as pd

def test_get_filtered_country_mapping():
    filtered_countries = get_filtered_country_mapping()
    
    # Check that the result is a DataFrame
    assert isinstance(filtered_countries, pd.DataFrame), "Result should be a pandas DataFrame"
    
    # Check that the DataFrame is not empty
    assert not filtered_countries.empty, "Filtered country mapping should not be empty"

test_get_filtered_country_mapping()