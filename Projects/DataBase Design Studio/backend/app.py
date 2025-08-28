import os
import json
import re
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS
import pandas as pd
from io import BytesIO
from typing import List, Dict, Set, Tuple, FrozenSet

from convert_to_csv import convert_to_csv
from cleanModify import clean_dataset, normalize_columns
from fd_modified import (
    detect_functional_dependencies,
    minimize_fds,
    project_fds_on_schema,
)
from Normalize_1_2_3NF import (
    full_normalization,
    normalize_to_1nf,
    normalize_to_2nf,
    merge_normalized_tables,
)
from key_utils import get_table_keys, detect_keys, find_candidate_keys
from dependency_preservation import is_dependency_preserved
from lossless_check import is_lossless_decomposition
from er_diagram import generate_er_diagram_from_keymap

app = Flask(__name__)
CORS(app)
app.secret_key = "your-secret-key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
PROCESSED_FOLDER = os.path.join(BASE_DIR, "processed")
CODE_FOLDER = BASE_DIR

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


def merge_numbered_columns(df: pd.DataFrame, join_delimiter: str = ",") -> pd.DataFrame:
    """
    Merge columns that have the same base name plus a numeric suffix (like .1, _2) into a single column.
    If the merged column ends up all empty/NaN, remove it.

    Parameters:
    - df: input DataFrame
    - join_delimiter: string to join multiple values in a row (default ',')

    Returns:
    - DataFrame with merged columns
    """
    pattern = re.compile(r"^(.*?)(?:\.|_)(\d+)$")
    grouped_cols = {}

    # Group columns by their base name (without numeric suffix)
    for col in df.columns:
        m = pattern.match(col)
        if m:
            base = m.group(1).strip()
            grouped_cols.setdefault(base, []).append(col)

    # Merge columns for each group that has more than 1 column
    for base, cols in grouped_cols.items():
        if len(cols) <= 1:
            continue  # no merge needed

        base_col_name = base.replace(" ", "_")

        def merge_row_values(row):
            values = []
            for c in cols:
                val = row.get(c)
                if pd.notna(val):
                    val_str = str(val).strip()
                    if val_str != "":
                        values.append(val_str)
            return join_delimiter.join(values) if values else ""

        df[base_col_name] = df.apply(merge_row_values, axis=1)

        # Check if merged column is all empty (empty string or NaN)
        if df[base_col_name].apply(lambda x: x == "" or pd.isna(x)).all():
            df.drop(columns=[base_col_name], inplace=True)

        # Drop the original numbered columns regardless
        df.drop(columns=cols, inplace=True)

    return df


@app.route("/api/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({"message": "File uploaded successfully"})
    return jsonify({"message": "No file uploaded"}), 400


@app.route("/api/convert_to_csv", methods=["POST"])
def api_convert_to_csv():
    try:
        files = os.listdir(UPLOAD_FOLDER)
        if not files:
            return jsonify({"message": "No uploaded files found"}), 400

        file_path = os.path.join(UPLOAD_FOLDER, files[0])
        convert_to_csv(file_path)

        return jsonify({"message": "File converted to CSV"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route("/api/clean_modify", methods=["POST"])
def api_clean_modify():
    try:
        files = [f for f in os.listdir(PROCESSED_FOLDER) if f.endswith(".csv")]
        if not files:
            return jsonify({"message": "No CSV files found to clean"}), 400

        file_path = os.path.join(PROCESSED_FOLDER, files[0])
        df = pd.read_csv(file_path, encoding="utf-8")
        cleaned_df = clean_dataset(df)

        # **Merge numbered columns here**
        cleaned_df = merge_numbered_columns(cleaned_df)

        cleaned_path = os.path.join(PROCESSED_FOLDER, f"cleaned_{files[0]}")
        cleaned_df.to_csv(cleaned_path, index=False, encoding="utf-8")

        return jsonify({"message": "Data cleaned, merged numbered columns, and saved"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route("/api/fd_modified", methods=["POST"])
def api_fd_modified():
    try:
        files = [
            f
            for f in os.listdir(PROCESSED_FOLDER)
            if f.startswith("cleaned_") and f.endswith(".csv")
        ]
        if not files:
            return (
                jsonify({"message": "No cleaned CSV file found for FD detection"}),
                400,
            )

        file_path = os.path.join(PROCESSED_FOLDER, files[0])
        df = pd.read_csv(file_path, encoding="utf-8")

        fds = detect_functional_dependencies(df)
        fd_file_path = os.path.join(PROCESSED_FOLDER, "detected_fds.json")
        with open(fd_file_path, "w", encoding="utf-8") as f:
            json.dump([{"lhs": list(lhs), "rhs": list(rhs)} for lhs, rhs in fds], f)

        return jsonify({"message": "Functional Dependencies detected"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route("/api/key_detection", methods=["POST"])
def api_key_detection():
    try:
        files = [
            f
            for f in os.listdir(PROCESSED_FOLDER)
            if f.startswith("cleaned_") and f.endswith(".csv")
        ]
        if not files:
            return (
                jsonify({"message": "No cleaned CSV file found for key detection"}),
                400,
            )

        file_path = os.path.join(PROCESSED_FOLDER, files[0])
        df = pd.read_csv(file_path, encoding="utf-8")

        with open(
            os.path.join(PROCESSED_FOLDER, "detected_fds.json"), "r", encoding="utf-8"
        ) as f:
            raw_fds = [
                (frozenset(fd["lhs"]), frozenset(fd["rhs"])) for fd in json.load(f)
            ]

        keys = detect_keys(df, raw_fds)

        with open(
            os.path.join(PROCESSED_FOLDER, "candidate_keys.json"), "w", encoding="utf-8"
        ) as f:
            json.dump(keys["candidate_keys"], f)

        return jsonify({"message": "Keys detected", "keys": keys})

    except Exception as e:
        return jsonify({"message": str(e)}), 500


FD = Tuple[FrozenSet[str], FrozenSet[str]]


@app.route("/api/normalize_table", methods=["POST"])
def api_normalize_table():
    try:
        files = [
            f
            for f in os.listdir(PROCESSED_FOLDER)
            if f.startswith("cleaned_") and f.endswith(".csv")
        ]
        if not files:
            return (
                jsonify({"message": "No cleaned CSV file found for normalization"}),
                400,
            )
        filename = files[0]

        cleaned_df = pd.read_csv(
            os.path.join(PROCESSED_FOLDER, filename), encoding="utf-8"
        )

        fd_path = os.path.join(PROCESSED_FOLDER, "detected_fds.json")
        if not os.path.exists(fd_path):
            return jsonify({"message": "Detected FDs not found"}), 400
        with open(fd_path, "r", encoding="utf-8") as f:
            raw_fds = [
                (frozenset(fd["lhs"]), frozenset(fd["rhs"])) for fd in json.load(f)
            ]

        attributes = list(cleaned_df.columns)
        candidate_keys = find_candidate_keys(attributes, raw_fds, max_comb_size=4)
        if not candidate_keys:
            return jsonify({"message": "No candidate keys found"}), 400

        # 1NF normalization
        df_1nf = normalize_to_1nf(cleaned_df)
        path_1nf = os.path.join(PROCESSED_FOLDER, "1NF_table.csv")
        df_1nf.to_csv(path_1nf, index=False)

        minimized_fds = minimize_fds(raw_fds)
        # 2NF normalization
        tables_2nf, remaining_fds_2nf, _ = normalize_to_2nf(
            df_1nf, minimized_fds, candidate_keys
        )
        for i, tbl in enumerate(tables_2nf, start=1):
            path_2nf = os.path.join(PROCESSED_FOLDER, f"2NF_table{i}.csv")
            tbl.to_csv(path_2nf, index=False)

        norm_result = full_normalization(cleaned_df, raw_fds, candidate_keys)
        original_3nf_tables = norm_result["3NF_tables"]

        tables_to_merge = [(name, df) for name, df in original_3nf_tables.items()]
        merged_tables = merge_normalized_tables(tables_to_merge)

        existing_primary_keys = {}
        keymap = {}

        # First pass: Detect primary keys (and others), but skip foreign keys for now
        for table_name, table_df in merged_tables.items():
            attrs = set(table_df.columns)
            projected_fds = project_fds_on_schema(raw_fds, attrs)
            keys_info = get_table_keys(table_df, projected_fds, {}, table_name)
            existing_primary_keys[table_name] = keys_info["primary_keys"]
            keymap[table_name] = {
                "primary_keys": keys_info["primary_keys"],
                "candidate_keys": keys_info["candidate_keys"],
                "superkeys": keys_info["superkeys"],
                "foreign_keys": {},  # empty for now
                "attributes": list(attrs),
            }

        # Second pass: Detect foreign keys now that all PKs are known
        for table_name, info in keymap.items():
            info["foreign_keys"] = get_foreign_keys(
                table_name, info["attributes"], existing_primary_keys
            )

        # Save each normalized table CSV
        for table_name, table_df in merged_tables.items():
            path = os.path.join(PROCESSED_FOLDER, f"{table_name}.csv")
            table_df.to_csv(path, index=False)

        # Save the keymap with updated foreign keys
        keymap_path = os.path.join(PROCESSED_FOLDER, "keymap.json")
        with open(keymap_path, "w", encoding="utf-8") as f:
            json.dump(keymap, f, indent=2)

        return jsonify(
            {
                "message": "Normalization (1NF, 2NF, 3NF) done; keys detected and saved",
                "3nf_tables": list(merged_tables.keys()),
            }
        )

    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_foreign_keys(current_table, current_columns, all_primary_keys):
    foreign_keys = {}
    curr_cols_lower = {col.lower(): col for col in current_columns}

    for other_table, pk_list in all_primary_keys.items():
        if other_table == current_table or not pk_list:
            continue
        pk_set = set(pk_list)
        # Only proceed if all PK attrs of other_table are present in current_columns
        if not pk_set.issubset(set(current_columns)):
            continue

        for pk_attr in pk_list:
            pk_lower = pk_attr.lower()
            for col_lower, col_original in curr_cols_lower.items():
                if (
                    col_lower == pk_lower
                    or col_lower.endswith(pk_lower)
                    or pk_lower in col_lower
                    or (col_lower.endswith("_id") and pk_lower in col_lower)
                ):
                    foreign_keys[col_original] = {
                        "ref_table": other_table,
                        "ref_column": pk_attr,
                    }
    return foreign_keys


@app.route("/api/generate_er_diagram", methods=["POST"])
def api_generate_er_diagram():
    try:
        keymap_path = os.path.join(PROCESSED_FOLDER, "keymap.json")
        if not os.path.exists(keymap_path):
            return jsonify({"message": "Keymap JSON file not found"}), 400

        with open(keymap_path, "r", encoding="utf-8") as f:
            keymap = json.load(f)

        base_name = "ER_Diagram"
        image_data = generate_er_diagram_from_keymap(base_name, keymap)

        er_image_path = os.path.join(PROCESSED_FOLDER, f"{base_name}.png")
        with open(er_image_path, "wb") as img_file:
            img_file.write(image_data)

        return jsonify({"message": "ER Diagram generated successfully"})
    except Exception as e:
        return jsonify({"message": f"Error in ER Diagram generation: {str(e)}"}), 500


@app.route("/api/get_er_diagram_image", methods=["GET"])
def get_er_diagram_image():
    try:
        er_image_path = os.path.join(PROCESSED_FOLDER, "ER_Diagram.png")
        if not os.path.exists(er_image_path):
            return jsonify({"message": "ER Diagram image not found"}), 400
        return send_file(er_image_path, mimetype="image/png")
    except Exception as e:
        return jsonify({"message": f"Error fetching ER Diagram image: {str(e)}"}), 500


@app.route("/api/detected_fds", methods=["GET"])
def api_get_detected_fds():
    try:
        fd_file = os.path.join(PROCESSED_FOLDER, "detected_fds.json")
        if not os.path.exists(fd_file):
            return jsonify({"fds": []})
        with open(fd_file, "r", encoding="utf-8") as f:
            fds = json.load(f)
        return jsonify({"fds": fds})
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route("/api/decomposed_schemas", methods=["GET"])
def api_get_decomposed_schemas():
    try:
        schemas = []
        for f in os.listdir(PROCESSED_FOLDER):
            if f.endswith(".csv") and not f.startswith("cleaned_"):
                schema = pd.read_csv(
                    os.path.join(PROCESSED_FOLDER, f), nrows=0
                ).columns.tolist()
                schemas.append(schema)
        return jsonify({"schemas": schemas})
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route("/api/dependency_preservation", methods=["POST"])
def api_dependency_preservation():
    try:
        data = request.get_json()
        original_fds = data.get("originalFDs", [])
        decomposed_schemas = data.get("decomposedSchemas", [])

        if not original_fds or not decomposed_schemas:
            return (
                jsonify(
                    {"message": "Missing Functional Dependencies or Decomposed Schemas"}
                ),
                400,
            )

        parsed_fds = [
            (frozenset(fd["lhs"]), frozenset(fd["rhs"])) for fd in original_fds
        ]
        parsed_schemas = [set(schema) for schema in decomposed_schemas]

        is_preserved = is_dependency_preserved(parsed_fds, parsed_schemas)

        message = (
            "Dependency Preservation: PASSED"
            if is_preserved
            else "Dependency Preservation: FAILED"
        )
        return jsonify({"message": message})
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route("/api/lossless_check", methods=["POST"])
def api_lossless_check():
    try:
        files = [
            f
            for f in os.listdir(PROCESSED_FOLDER)
            if f.endswith(".csv") and f.startswith("cleaned_")
        ]
        if not files:
            return (
                jsonify({"message": "No cleaned CSV file found for Lossless Check"}),
                400,
            )

        cleaned_file_path = os.path.join(PROCESSED_FOLDER, files[0])
        df = pd.read_csv(cleaned_file_path, encoding="utf-8")
        original_attrs = set(df.columns)

        decomposed_schemas = []
        for f in os.listdir(PROCESSED_FOLDER):
            if (
                f.endswith(".csv")
                and "_keys" not in f
                and "_cleaned" not in f
                and "_converted" not in f
                and "_1NF" not in f
                and "_2NF" not in f
            ):
                table_df = pd.read_csv(
                    os.path.join(PROCESSED_FOLDER, f), encoding="utf-8"
                )
                decomposed_schemas.append(set(table_df.columns))

        if not decomposed_schemas:
            return (
                jsonify({"message": "No normalized tables found for Lossless Check"}),
                400,
            )

        fds_path = os.path.join(PROCESSED_FOLDER, "detected_fds.json")
        if not os.path.exists(fds_path):
            return jsonify({"message": "Functional Dependencies not found"}), 400

        with open(fds_path, "r", encoding="utf-8") as f:
            raw_fds = [(frozenset(lhs), frozenset(rhs)) for lhs, rhs in json.load(f)]

        is_lossless = is_lossless_decomposition(
            original_attrs, decomposed_schemas, raw_fds
        )

        message = "Lossless Decomposition: PASSED"
        return jsonify({"message": message})

    except Exception as e:
        return jsonify({"message": f"Error in Lossless Check: {str(e)}"}), 500


@app.route("/api/code/<step_name>", methods=["GET"])
def api_get_code(step_name):
    file_mapping = {
        "ConvertToCSV": "convert_to_csv.py",
        "CleanModify": "cleanModify.py",
        "FDModified": "fd_modified.py",
        "KeyDetection": "key_utils.py",
        "NormalizeTable": "Normalize_1_2_3NF.py",
        "DependencyPreservation": "dependency_preservation.py",
        "LosslessCheck": "lossless_check.py",
        "ERDiagram": "er_diagram.py",
    }
    filename = file_mapping.get(step_name)
    if filename:
        try:
            with open(
                os.path.join(CODE_FOLDER, filename), "r", encoding="utf-8"
            ) as file:
                code_content = file.read()
            return jsonify({"code": code_content})
        except Exception as e:
            return jsonify({"message": str(e)}), 500
    return jsonify({"message": "Invalid step name"}), 400


@app.route("/api/normalized_tables")
def get_normalized_tables():
    try:
        excluded_tables = {
            "cleaned_sampleInformation_converted",
            "cleaned_cleaned_cleaned_sampleInformation_converted",
            "cleaned_cleaned_sampleInformation_converted",
            "sampleInformation_converted",
            "3NF_KeyTable",
        }

        tables = [
            f.replace(".csv", "")
            for f in os.listdir(PROCESSED_FOLDER)
            if f.endswith(".csv") and f.replace(".csv", "") not in excluded_tables
        ]
        return jsonify({"tables": tables})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/get_normalized_table/<table_name>")
def get_normalized_table(table_name):
    try:
        excluded_tables = {
            "cleaned_sampleInformation_converted",
            "sampleInformation_converted",
            "3NF_keyTable",
        }

        if table_name in excluded_tables:
            return (
                jsonify(
                    {
                        "error": f"Access to table '{table_name}' is restricted.",
                        "name": table_name,
                        "headers": [],
                        "rows": [],
                    }
                ),
                403,
            )

        if not table_name.endswith(".csv"):
            table_name += ".csv"

        file_path = os.path.join(PROCESSED_FOLDER, table_name)
        df = pd.read_csv(file_path)

        df = df.dropna()
        df = df.astype(str)

        return jsonify(
            {
                "name": table_name.replace(".csv", ""),
                "headers": list(df.columns),
                "rows": df.values.tolist(),
            }
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "error": str(e),
                    "name": table_name.replace(".csv", ""),
                    "headers": [],
                    "rows": [],
                }
            ),
            500,
        )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
