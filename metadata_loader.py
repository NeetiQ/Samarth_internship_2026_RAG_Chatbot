import pandas as pd
import os

def load_metadata(filepath: str) -> pd.DataFrame:
    """
    Loads and cleans metadata from the specified parquet file.
    
    Args:
        filepath: Absolute or relative path to the metadata.parquet file.
        
    Returns:
        pd.DataFrame: A cleaned Pandas DataFrame containing metadata.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Metadata file not found at: {filepath}")
        
    df = pd.read_parquet(filepath)
    
    # Standardize column types as strings to avoid typing/serialization issues downstream
    # except for any numeric fields we want to keep, but since everything in the source is string,
    # converting them systematically to string is very safe.
    for col in df.columns:
        df[col] = df[col].fillna("").astype(str)
        # Clean up pandas object/string representations of null like "<NA>" or "nan" or "None"
        df[col] = df[col].replace({"<NA>": "", "nan": "", "None": ""})
        
    return df
