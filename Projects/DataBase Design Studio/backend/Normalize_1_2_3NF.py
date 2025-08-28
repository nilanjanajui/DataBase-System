from typing import List, Dict, Set, Tuple, FrozenSet
import pandas as pd
from fd_modified import minimize_fds, project_fds_on_schema
from key_utils import find_candidate_keys, get_table_keys
from cleanModify import normalize_columns
from collections import defaultdict

FD = Tuple[FrozenSet[str], FrozenSet[str]]


def closure(attrs: Set[str], fds: List[FD]) -> Set[str]:
    result = set(attrs)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs.issubset(result) and not rhs.issubset(result):
                result.update(rhs)
                changed = True
    return result


def is_partial_dependency(fd: FD, candidate_keys: List[Set[str]]) -> bool:
    lhs = fd[0]
    for key in candidate_keys:
        if lhs < key:
            return True
    return False


def is_transitive_dependency(
    fd: FD, candidate_keys: List[Set[str]], prime_attrs: Set[str]
) -> bool:
    lhs, rhs = fd
    lhs_is_superkey = any(lhs.issuperset(key) for key in candidate_keys)
    rhs_has_nonprime = any(attr not in prime_attrs for attr in rhs)
    return not lhs_is_superkey and rhs_has_nonprime


def normalize_to_1nf(df: pd.DataFrame) -> pd.DataFrame:
    df_1nf = df.copy()
    for col in df_1nf.columns:
        if df_1nf[col].apply(lambda x: isinstance(x, str) and "," in x).any():
            df_1nf = (
                df_1nf.drop(columns=[col])
                .join(
                    df_1nf[col]
                    .str.split(",", expand=True)
                    .stack()
                    .reset_index(level=1, drop=True)
                    .rename(col)
                )
                .reset_index(drop=True)
            )
    return df_1nf.drop_duplicates()


def normalize_to_2nf(
    df: pd.DataFrame, fds: List[FD], candidate_keys: List[Set[str]]
) -> Tuple[List[pd.DataFrame], List[FD], List[FD]]:
    tables, remaining_fds, removed_fds = [], [], []
    for fd in fds:
        if is_partial_dependency(fd, candidate_keys):
            lhs, rhs = fd
            table_attrs = lhs.union(rhs)

            # FIX: Validate columns exist before selection
            missing_cols = [col for col in table_attrs if col not in df.columns]
            if missing_cols:
                raise ValueError(
                    f"Missing columns in df for 2NF normalization: {missing_cols}"
                )

            # FIX: convert set to list before indexing
            cols_to_select = list(table_attrs)
            new_table = df[cols_to_select].drop_duplicates()
            tables.append(new_table)
            removed_fds.append(fd)
        else:
            remaining_fds.append(fd)
    return tables, remaining_fds, removed_fds


def normalize_to_3nf(
    df: pd.DataFrame, fds: List[FD], candidate_keys: List[Set[str]]
) -> Tuple[List[pd.DataFrame], List[FD], List[FD]]:
    prime_attrs = set().union(*candidate_keys)
    tables, removed_fds, remaining_fds = [], [], []
    for fd in fds:
        if is_transitive_dependency(fd, candidate_keys, prime_attrs):
            lhs, rhs = fd
            table_attrs = lhs.union(rhs)

            # FIX: Validate columns exist before selection
            missing_cols = [col for col in table_attrs if col not in df.columns]
            if missing_cols:
                raise ValueError(
                    f"Missing columns in df for 3NF normalization: {missing_cols}"
                )

            cols_to_select = list(table_attrs)
            new_table = df[cols_to_select].drop_duplicates()
            tables.append(new_table)
            removed_fds.append(fd)
        else:
            remaining_fds.append(fd)
    return tables, remaining_fds, removed_fds


def full_normalization(
    df: pd.DataFrame, raw_fds: List[FD], global_candidate_keys: List[Set[str]]
) -> Dict:
    df.columns = normalize_columns(df.columns)
    global_candidate_keys = [
        set(normalize_columns(list(key))) for key in global_candidate_keys
    ]

    minimized_fds = minimize_fds(raw_fds)
    all_attributes = set(df.columns)

    result_tables = {}
    projected_fds_per_table = {}
    primary_keys_per_table = {}
    foreign_keys_per_table = {}

    used_attributes = set()
    table_index = 1

    # --- STEP 1: Synthesize 3NF Tables using FD Groups ---
    for lhs, rhs in minimized_fds:
        schema = lhs.union(rhs)
        missing_cols = [col for col in schema if col not in df.columns]
        if missing_cols:
            raise ValueError(
                f"Missing columns in df for table {table_index}: {missing_cols}"
            )

        table_name = f"3NF_Table{table_index}"
        table_df = df[list(schema)].drop_duplicates().reset_index(drop=True)

        result_tables[table_name] = table_df
        projected_fds_per_table[table_name] = [(lhs, rhs)]

        used_attributes.update(schema)
        table_index += 1

    # --- STEP 2: Ensure at least one table contains a Candidate Key ---
    key_covered = any(
        any(key.issubset(set(t.columns)) for t in result_tables.values())
        for key in global_candidate_keys
    )

    if not key_covered and global_candidate_keys:
        smallest_key = min(global_candidate_keys, key=len)
        missing_cols = [col for col in smallest_key if col not in df.columns]
        if missing_cols:
            print(
                f"Warning: Candidate key {sorted(smallest_key)} not present in df.columns. Skipping Key Table creation."
            )
        else:
            table_name = "3NF_KeyTable"
            key_df = df[list(smallest_key)].drop_duplicates().reset_index(drop=True)
            result_tables[table_name] = key_df
            projected_fds_per_table[table_name] = []

    # --- DEBUG PRINTS ---
    print(f"DataFrame Columns: {df.columns.tolist()}")
    print(f"Candidate Keys: {[sorted(list(k)) for k in global_candidate_keys]}")

    # --- STEP 3: Per-Table Key Detection (PK, CK, SK, FK) ---
    all_primary_keys_global = {}  # Used for FK Detection across tables

    # First Pass: Detect Primary Keys only
    for table_name, table_df in result_tables.items():
        table_schema = set(table_df.columns)
        table_fds = project_fds_on_schema(minimized_fds, table_schema)

        keys_info = get_table_keys(
            df=table_df,
            fds=table_fds,
            existing_primary_keys={},
            table_name=table_name,
        )

        primary_keys_per_table[table_name] = keys_info["primary_keys"]
        all_primary_keys_global[table_name] = keys_info["primary_keys"]

    # Second Pass: Detect Foreign Keys using Global PKs Map
    for table_name, table_df in result_tables.items():
        table_schema = set(table_df.columns)
        table_fds = project_fds_on_schema(minimized_fds, table_schema)

        keys_info = get_table_keys(
            df=table_df,
            fds=table_fds,
            existing_primary_keys=all_primary_keys_global,
            table_name=table_name,
        )

        foreign_keys_per_table[table_name] = keys_info["foreign_keys"]
        primary_keys_per_table[table_name] = keys_info["primary_keys"]

    # --- STEP 4: Remove Redundant Tables ---
    tables_to_remove = set()
    table_schemas = {name: set(table.columns) for name, table in result_tables.items()}

    for name1, schema1 in table_schemas.items():
        for name2, schema2 in table_schemas.items():
            if name1 != name2 and schema1.issubset(schema2):
                tables_to_remove.add(name1)
                break

    for table_name in tables_to_remove:
        del result_tables[table_name]
        del projected_fds_per_table[table_name]
        del primary_keys_per_table[table_name]
        if table_name in foreign_keys_per_table:
            del foreign_keys_per_table[table_name]

    # --- FINAL RETURN ---
    return {
        "3NF_tables": result_tables,
        "projected_fds": projected_fds_per_table,
        "primary_keys": primary_keys_per_table,
        "foreign_keys": foreign_keys_per_table,
    }


def merge_normalized_tables(
    tables: List[Tuple[str, pd.DataFrame]],
) -> Dict[str, pd.DataFrame]:
    from cleanModify import (
        normalize_columns,
    )  # Import normalize_columns function if in separate file

    merged_tables = {}

    for name, table in tables:
        # FIX: Normalize columns before using as merge key
        normalized_cols = tuple(sorted(normalize_columns(table.columns)))

        # FIX: Normalize table columns BEFORE using as dict key to avoid mismatch
        table.columns = normalize_columns(table.columns)

        if normalized_cols in merged_tables:
            merged_tables[normalized_cols] = pd.concat(
                [merged_tables[normalized_cols], table], ignore_index=True
            )
        else:
            merged_tables[normalized_cols] = table.copy()

    final_tables = {}
    for i, (col_key, df) in enumerate(merged_tables.items(), 1):
        final_tables[f"3NF_table{i}"] = df.drop_duplicates().reset_index(drop=True)

    return final_tables
