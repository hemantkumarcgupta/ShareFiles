#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 22:50:26 2025

@author: hemantcgupta
"""


import pandas as pd
import polars as pl
# =============================================================================
# functions
# =============================================================================
def auto_fix_header(df: pl.DataFrame, min_fill: float = 0.8) -> pl.DataFrame:
    """
    Automatically detect and promote header row **only if**
    current column names are blank, None, or generic.
    """
    # Check if all columns are empty, None, or unnamed
    if any("unnamed" in str(c).lower() or str(c).strip() in ("", "none") for c in df.columns):
        header_idx = detect_header_row(df, min_fill=min_fill)
        df = promote_header(df, header_idx)
        print(f"Auto header applied at row {header_idx}")
    else:
        print("Existing header detected — no change made.")
    df = df.select([pl.col(col).cast(pl.Utf8) for col in df.columns])
    return df
    
def merge_excel_sheets(file_path: str) -> pl.DataFrame:
    sheets = pl.read_excel(file_path, sheet_id=0)
    sheets = {k: auto_fix_header(df) for k, df in sheets.items()}
    all_cols = sorted({c for df in sheets.values() for c in df.columns})
    return pl.concat(
        [df.with_columns([pl.lit(None).alias(c) for c in all_cols if c not in df.columns])
           .select(all_cols) for df in sheets.values()],
        how="vertical"
    )

def detect_header_row(df: pl.DataFrame, min_fill: float = 0.8) -> int:
    """
    Detects the most likely header row index based on non-empty cell ratio.
    Returns the row index (0-based).
    """
    data = df.to_numpy()
    n_rows, n_cols = data.shape
    for i in range(n_rows):
        non_empty = (data[i] != None) & (data[i] != "") & (data[i] != "nan")
        fill_ratio = non_empty.sum() / n_cols
        if fill_ratio >= min_fill:
            return i
    return 0  


def promote_header(df: pl.DataFrame, header_idx: int) -> pl.DataFrame:
    """
    Promote the given row as column names, and return remaining rows as data.
    """
    new_cols = [str(x).strip() for x in df.row(header_idx)]
    df = df.slice(header_idx + 1)
    df.columns = new_cols
    return df

file_path = "test28L.xlsx"
df = merge_excel_sheets(file_path)
df.write_parquet("test28L.parquet")




# =============================================================================
# 
# =============================================================================

# import pandas as pd
# import polars as pl
# # Read all Excel sheets efficiently and combine
# file = "stock.xlsx"
# sheets = pl.read_excel(file, sheet_id=0)  # Returns dict of sheets
# df = pd.concat([df.to_pandas() for df in sheets.values()]).reset_index(drop=True)


# df = pd.concat([df for _ in range(100)])
# max_rows = 1_048_500
# with pd.ExcelWriter('test28L.xlsx', engine='openpyxl') as writer:
#     for i in range(0, len(df), max_rows):
#         sheet_name = f'Sheet_{i // max_rows + 1}'
#         df.iloc[i:i+max_rows].to_excel(writer, index=False, sheet_name=sheet_name)

# # df.to_parquet("test28L.parquet", index=False)

# df = pd.read_parquet('test28L.parquet')







