import pandas as pd
import sys

try:
    # Assuming the first row is not a header
    df = pd.read_excel("sheet.xlsx", header=None)
    # Excel rows are 1-based, pandas iloc is 0-based
    rows_data = df.iloc[29:31]
    print("--- Data from sheet.xlsx (Rows 30 and 31) ---")
    # Print data row by row for clarity
    for index, row in rows_data.iterrows():
        # Convert row data to list, handling potential NaN values
        row_list = [item if pd.notna(item) else "" for item in row.tolist()]
        print(f"Row {index + 1}: {row_list}")
    print("---------------------------------------------")
except FileNotFoundError:
    print("Error: sheet.xlsx not found in the current directory.", file=sys.stderr)
    sys.exit(1)
except ImportError:
    print(
        "Error: pandas library not found. Please ensure it is installed (pip install pandas).",
        file=sys.stderr,
    )
    sys.exit(1)
except Exception as e:
    print(f"An error occurred while reading sheet.xlsx: {e}", file=sys.stderr)
    sys.exit(1)
