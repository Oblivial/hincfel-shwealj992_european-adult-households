import pandas as pd

def stfeco_by_country_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform and filter ESS Data and return a DataFrame.
    Dataframe contains shares of stfeco values by country and year.
    
    Parameter
    ---------
    df : pandas.DataFrame
        ESS-Dataset

    Returns
    -------
    pandas.DataFrame
        Rows:
        - country
        - ess round
        - year
        - stfeco value
        - share of each stfeco value
    """

    # Create a copy to avoid modifying the original
    data = df.copy()
    
    # Remove rows with missing stfeco or interview year values
    data = data.dropna(subset=['stfeco', 'inwyr'])
    
    # Group by country, essround, year, and stfeco value, then count occurrences
    grouped = data.groupby(['cntry', 'essround', 'inwyr', 'stfeco']).size().reset_index(name='count')
    
    # Calculate total for each country-essround-year combination
    totals = grouped.groupby(['cntry', 'essround', 'inwyr'])['count'].sum().reset_index(name='total')
    
    # Merge totals back and calculate share
    result = grouped.merge(totals, on=['cntry', 'essround', 'inwyr'])
    result['share'] = result['count'] / result['total']
    
    # Select and rename columns as per the docstring
    result = result[['cntry', 'essround', 'inwyr', 'stfeco', 'share']].copy()
    result.columns = ['country', 'essround', 'year', 'stfeco_value', 'share']
    
    # Sort by country, essround, year, and stfeco value for consistent output
    result = result.sort_values(['country', 'essround', 'year', 'stfeco_value']).reset_index(drop=True)
    
    return result