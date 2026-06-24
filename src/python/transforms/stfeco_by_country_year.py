import pandas as pd

from util import get_ess_rounds


def _essround_to_year(essround: str) -> int:
    if pd.isna(essround):
        return None

    rounds = get_ess_rounds()
    ess_string = "ESS" + str(essround)
    try:
        year = rounds[ess_string]
        return year
    except KeyError:
        print(f"Error!: {ess_string} does not exist in the configuration or is configured poorly")
        return None


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

    # Remove rows with missing stfeco
    data = data.dropna(subset=['stfeco'])

    if 'essround' not in data.columns:
        raise ValueError("Input data must contain an 'essround' column")

    data['year'] = data['essround'].apply(_essround_to_year)
    data = data.dropna(subset=['year'])

    # Group by country, essround, year, and stfeco value, then count occurrences
    grouped = data.groupby(['cntry', 'essround', 'year', 'stfeco']).size().reset_index(name='count')

    # Calculate total for each country-essround-year combination
    totals = grouped.groupby(['cntry', 'essround', 'year'])['count'].sum().reset_index(name='total')

    # Merge totals back and calculate share
    result = grouped.merge(totals, on=['cntry', 'essround', 'year'])
    result['share'] = result['count'] / result['total']

    # Select and rename columns as per the docstring
    result = result[['cntry', 'essround', 'year', 'stfeco', 'share']].copy()
    result.columns = ['country', 'essround', 'year', 'stfeco_value', 'share']
    
    # Sort by country, essround, year, and stfeco value for consistent output
    result = result.sort_values(['country', 'essround', 'year', 'stfeco_value']).reset_index(drop=True)
    
    return result