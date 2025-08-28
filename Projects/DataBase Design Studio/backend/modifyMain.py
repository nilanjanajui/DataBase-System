import os
import pandas as pd
from collections import defaultdict
from typing import List, Tuple, FrozenSet

from convert_to_csv import convert_to_csv
from cleanModify import clean_dataset
from fd_modified import detect_functional_dependencies, minimize_fds, closure
from Normalize_1_2_3NF import full_normalization
from key_utils import find_candidate_keys, find_superkeys

# Type alias
FD = Tuple[FrozenSet[str], FrozenSet[str]]

# Paths setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "uploads")
PROCESSED_FOLDER = os.path.join(BASE_DIR, "processed")

os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def group_fds(fds: List[FD]) -> dict:
    fd_dict = defaultdict(set)
    for lhs, rhs in fds:
        fd_dict[frozenset(lhs)].update(rhs)
    return dict(fd_dict)

def process_file(file_path: str, filename: str):
    print(f"\n🟡 Processing: {filename}")

    # Step 1: Convert to CSV
    csv_path, df = convert_to_csv(file_path, output_folder=PROCESSED_FOLDER)

    # Step 2: Clean data
    cleaned_df = clean_dataset(df)
    cleaned_name = os.path.splitext(filename)[0] + "_cleaned.csv"
    cleaned_path = os.path.join(PROCESSED_FOLDER, cleaned_name)
    cleaned_df.to_csv(cleaned_path, index=False)

    # Step 3: Detect & minimize FDs
    raw_fds = detect_functional_dependencies(cleaned_df)
    minimized_fds = minimize_fds(raw_fds)
    grouped_fds = group_fds(minimized_fds)

    print("📌 Detected Functional Dependencies:")
    for lhs, rhs in grouped_fds.items():
        print(f"  {set(lhs)} -> {rhs}")

    # Step 4: Closure of sample attribute
    sample_attrs = set(cleaned_df.columns[:1])
    closure_set = closure(sample_attrs, minimized_fds)
    print(f"📦 Closure of {sample_attrs}: {closure_set}")

    # Step 5: Find candidate keys
    attributes = list(cleaned_df.columns)
    candidate_keys = find_candidate_keys(attributes, minimized_fds)

    if not candidate_keys:
        print("⚠️ No candidate keys found — normalization may be incomplete.")
        return

    # Step 6: Normalize
    normalization_result = full_normalization(cleaned_df, minimized_fds, candidate_keys)

    # Optional: Show removed dependencies
    print("\n🧹 Removed Dependencies:")
    for cond in normalization_result['conditions']['2NF'] + normalization_result['conditions']['3NF']:
        print(f"  - {cond}")

    # Step 7: Save normalized tables
    tables = normalization_result.get('3NF_tables', [])
    if not tables:
        print("⚠️ No 3NF tables generated.")
        return

    for i, table in enumerate(tables, start=1):
        out_name = f"{os.path.splitext(filename)[0]}_3NF_part{i}.csv"
        out_path = os.path.join(PROCESSED_FOLDER, out_name)
        table.to_csv(out_path, index=False)
        print(f"✅ Saved normalized table: {out_path}")

        # Step 8: Detect keys for this table
        sub_attrs = list(table.columns)
        sub_fds = [fd for fd in minimized_fds if fd[0].issubset(sub_attrs) and fd[1].issubset(sub_attrs)]
        sub_candidate_keys = find_candidate_keys(sub_attrs, sub_fds)
        sub_superkeys = find_superkeys(sub_candidate_keys, sub_attrs)
        primary_key = min(sub_candidate_keys, key=len) if sub_candidate_keys else None

        print(f"\n🔑 Keys for 3NF_part{i}:")
        print(f"  → Primary Key    : {primary_key}")
        print(f"  → Candidate Keys : {sub_candidate_keys}")
        print(f"  → Superkeys      : {sub_superkeys}")

# ---------------------
# Main processing loop
# ---------------------
for filename in os.listdir(DATA_FOLDER):
    if not filename.lower().endswith(('.xlsx', '.xls', '.csv', '.txt', '.json', '.xml')):
        continue
    if filename.endswith('_converted.csv'):
        continue

    file_path = os.path.join(DATA_FOLDER, filename)

    try:
        process_file(file_path, filename)
    except Exception as e:
        print(f"❌ Failed to process {filename}: {type(e).__name__}: {e}")
