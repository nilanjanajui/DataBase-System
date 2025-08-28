import pandas as pd
import re


def normalize_columns(columns):
    # Strip whitespace, remove trailing dots, convert to lowercase, replace spaces with underscores
    return [col.strip().rstrip(".").lower().replace(" ", "_") for col in columns]


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()

    # 1. Standardize column names: just lowercase + spaces → underscores
    df_clean.columns = (
        df_clean.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)
    )

    print("Columns after cleaning:", list(df_clean.columns))  # Debug print

    # 2. Remove duplicate rows
    df_clean = df_clean.drop_duplicates()

    # 3. Remove duplicate columns
    df_clean = df_clean.loc[:, ~df_clean.T.duplicated()]

    # 4. Clean each column's data
    for col in df_clean.columns:
        if df_clean[col].dtype == "object":
            df_clean[col] = df_clean[col].astype(str).str.strip().str.lower()
            df_clean[col] = df_clean[col].replace("", "unknown")
            df_clean[col] = df_clean[col].fillna("unknown")

        elif pd.api.types.is_datetime64_any_dtype(df_clean[col]):
            dt_col = pd.to_datetime(df_clean[col], errors="coerce")
            df_clean[col] = dt_col.where(dt_col.notna(), "unknown").astype(object)

        elif pd.api.types.is_numeric_dtype(df_clean[col]):
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
            df_clean[col] = df_clean[col].fillna(0)

        else:
            df_clean[col] = df_clean[col].fillna("unknown")

    # 5. Normalize object-type formats (e.g., dates/numbers stored as strings)
    df_clean = normalize_formats(df_clean)

    # 6. Final replacement of any remaining empty strings
    df_clean = df_clean.replace("", "unknown")

    return df_clean


def flatten_repeating_columns(df: pd.DataFrame) -> pd.DataFrame:
    df_flat = df.copy()

    # NO re-normalization of columns here — use as-is
    print("Columns before flattening:", list(df_flat.columns))  # Debug print

    # Group columns by base name (e.g., sideeffect, sideeffect1, sideeffect_2)
    grouped_cols = {}
    for col in df_flat.columns:
        # Match base name plus optional suffix digits (with or without underscore)
        match = re.match(r"^(.*?)(?:_?\d+)?$", col)
        if match:
            base = match.group(1)
            grouped_cols.setdefault(base, []).append(col)

    # Merge grouped columns into a single column if multiple exist
    for base, cols in grouped_cols.items():
        if len(cols) > 1:
            merged_name = base  # Keep base name
            # Combine all columns' non-empty values (lowercased)
            df_flat[merged_name] = (
                df_flat[cols]
                .astype(str)
                .fillna("")
                .apply(
                    lambda row: ", ".join(
                        val.strip().lower()
                        for val in row
                        if val.strip().lower() not in ["", "nan", "none", "unknown"]
                    ),
                    axis=1,
                )
            )
            # Drop old columns except merged
            for col in cols:
                if col != merged_name:
                    df_flat.drop(columns=col, inplace=True)

    print("Columns after flattening:", list(df_flat.columns))  # Debug print
    return df_flat


def normalize_formats(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if df[col].dtype == "object":
            if is_date_column(df[col]):
                df[col] = (
                    pd.to_datetime(df[col], errors="coerce")
                    .astype("object")
                    .fillna("unknown")
                )
            elif is_numeric_column(df[col]):
                df[col] = (
                    pd.to_numeric(df[col], errors="coerce")
                    .astype("object")
                    .fillna("unknown")
                )
    return df


def is_date_column(series: pd.Series) -> bool:
    sample = series.dropna().astype(str).head(10)
    patterns = [
        r"^\d{4}-\d{2}-\d{2}$",  # 2024-07-27
        r"^\d{2}/\d{2}/\d{4}$",  # 27/07/2024
        r"^\d{2}-\d{2}-\d{4}$",  # 27-07-2024
        r"^\d{4}/\d{2}/\d{2}$",  # 2024/07/27
        r"^[a-zA-Z]{3,9} \d{4}$",  # May 2024
        r"^[a-zA-Z]{3,9} \d{1,2}, \d{4}$",  # August 1, 2024
    ]
    return any(re.match(p, val.strip()) for val in sample for p in patterns)


def is_numeric_column(series: pd.Series) -> bool:
    sample = series.dropna().astype(str).head(10)
    return all(
        re.fullmatch(r"^-?\d+(\.\d+)?$", val.strip())
        for val in sample
        if val.strip() != ""
    )
