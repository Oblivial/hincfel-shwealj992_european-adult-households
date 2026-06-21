import pandas as pd

def shweal_by_country_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform and filter WID data and return a DataFrame.
    Dataframe contains shares of wealth held by the middle 40% ordered by country and year.
   
    Parameter
    ---------
    df : pandas.DataFrame
        WID-Datensatz eines Landes

    Returns
    -------
    pandas.DataFrame
        Spalten:
        - country
        - year
        - middle_class_share
    """
    country = df.iloc[0]["country"]

    middle = df[
        (df["variable"] == "shwealj992") &
        (df["percentile"] == "p50p90")
    ].copy()

    middle["value"] = pd.to_numeric(
        middle["value"].astype(str).str.replace(",", ".", regex=False),
        errors="raise"
    )

    result = (
        middle[["year", "value"]]
        .rename(columns={"value": "middle_class_wealth_share"})
        .sort_values("year")
        .reset_index(drop=True)
    )

    result.insert(0, "country", country)
    return result