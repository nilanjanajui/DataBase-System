from typing import List, Set, Tuple, FrozenSet, Dict
from itertools import combinations
import pandas as pd

# Type alias for Functional Dependency
FD = Tuple[FrozenSet[str], FrozenSet[str]]


def powerset(attributes: List[str], max_size: int = None) -> List[Set[str]]:
    """
    Generate powerset of attributes up to size `max_size`.
    """
    max_size = max_size or len(attributes)
    return [set(s) for i in range(1, max_size + 1) for s in combinations(attributes, i)]


def closure(attrs: Set[str], fds: List[FD]) -> Set[str]:
    """
    Compute attribute closure of attrs under the set of FDs.
    """
    result = set(attrs)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs.issubset(result) and not rhs.issubset(result):
                result.update(rhs)
                changed = True
    return result


def find_candidate_keys(
    attributes: List[str], fds: List[FD], max_comb_size: int = 5
) -> List[Set[str]]:
    """
    Find candidate keys for the relation.
    """
    all_attrs = set(attributes)
    candidate_keys = []

    for subset in powerset(attributes, max_comb_size):
        closure_set = closure(subset, fds)
        if closure_set == all_attrs:
            if not any(
                existing_key.issubset(subset) for existing_key in candidate_keys
            ):
                candidate_keys.append(set(subset))
    return candidate_keys


def find_superkeys(
    candidate_keys: List[Set[str]], attributes: List[str], max_comb_size: int = 5
) -> List[Set[str]]:
    """
    Generate superkeys based on candidate keys by adding extra attributes.
    """
    all_attrs = set(attributes)
    superkeys_set = set()
    for key in candidate_keys:
        remaining = all_attrs - key
        for extras in powerset(list(remaining), max_comb_size):
            superkey = frozenset(key.union(extras))
            superkeys_set.add(superkey)
        superkeys_set.add(frozenset(key))
    return [set(sk) for sk in sorted(superkeys_set, key=lambda x: (len(x), sorted(x)))]


def find_primary_keys(candidate_keys: List[Set[str]]) -> List[str]:
    """
    Return the minimal candidate key as the primary key.
    """
    if not candidate_keys:
        return []
    smallest_key = min(candidate_keys, key=len)
    return sorted(list(smallest_key))


def find_foreign_keys(
    current_table: str,
    current_columns: List[str],
    all_primary_keys: Dict[str, List[str]],
) -> Dict[str, str]:
    """
    Detect foreign keys by matching column names with primary keys of other tables.
    """
    foreign_keys = {}
    for col in current_columns:
        for table_name, pk_list in all_primary_keys.items():
            if table_name == current_table:
                continue
            for pk in pk_list:
                # Match exact or suffix/prefix with '_id' heuristic
                if (
                    col.lower() == pk.lower()
                    or col.lower().endswith(pk.lower())
                    or pk.lower() in col.lower()
                    or (col.lower().endswith("_id") and pk.lower() in col.lower())
                ):
                    foreign_keys[col] = table_name
    return foreign_keys


def detect_keys(
    df: pd.DataFrame,
    fds: List[FD],
    max_comb_size: int = 5,
) -> Dict[str, object]:
    """
    Detect candidate keys, primary key, and superkeys for a given DataFrame and FDs.
    """
    attributes = list(df.columns)
    candidate_keys = find_candidate_keys(attributes, fds, max_comb_size=max_comb_size)
    primary_key = find_primary_keys(candidate_keys)
    superkeys = find_superkeys(candidate_keys, attributes, max_comb_size=max_comb_size)
    return {
        "candidate_keys": [sorted(list(k)) for k in candidate_keys],
        "primary_key": primary_key,
        "superkeys": [sorted(list(sk)) for sk in superkeys],
    }


def get_table_keys(
    df: pd.DataFrame,
    fds: List[FD],
    existing_primary_keys: Dict[str, List[str]],
    table_name: str,
    max_comb_size: int = 4,
) -> Dict:
    """
    Detect keys for a table including:
    - Candidate keys (minimal keys that functionally determine all attributes)
    - Primary key (smallest candidate key)
    - Superkeys (candidate keys plus their supersets)
    - Foreign keys (columns referencing PKs in other tables)
    """

    attributes = list(df.columns)

    # Find candidate keys based on FDs and attribute list
    candidate_keys = find_candidate_keys(attributes, fds, max_comb_size=max_comb_size)

    # Primary key is the smallest candidate key (by length)
    primary_key = find_primary_keys(candidate_keys)

    # Compute superkeys: all supersets of candidate keys up to max_comb_size
    superkeys_set = set()
    all_attrs_set = set(attributes)
    for ck in candidate_keys:
        remaining = all_attrs_set - ck
        # Add supersets of candidate keys by adding extra attrs from remaining attributes
        for extras in powerset(list(remaining), max_comb_size):
            superkey = frozenset(ck.union(extras))
            superkeys_set.add(superkey)
        # Also add the candidate key itself as a superkey
        superkeys_set.add(frozenset(ck))

    # Convert frozensets to sorted lists for JSON serializable format
    superkeys = [sorted(list(sk)) for sk in superkeys_set]

    # Detect foreign keys by checking if PKs from other tables appear as columns here
    foreign_keys = get_foreign_keys(table_name, attributes, existing_primary_keys)

    return {
        "attributes": attributes,
        "primary_keys": primary_key,
        "candidate_keys": [sorted(list(k)) for k in candidate_keys],
        "superkeys": superkeys,
        "foreign_keys": foreign_keys,  # Now a dict: {fk_col: {"ref_table": ..., "ref_column": ...}}
    }


def get_foreign_keys(
    current_table: str,
    current_columns: List[str],
    all_primary_keys: Dict[str, List[str]],
) -> Dict[str, Dict[str, str]]:
    """
    Detect foreign keys by matching columns in current table to primary keys of other tables.
    Returns dict mapping FK column name to dict with referenced table and column.
    """
    foreign_keys = {}

    for other_table, pk_list in all_primary_keys.items():
        # Skip self table or empty PKs
        if other_table == current_table or not pk_list:
            continue

        pk_set = set(pk_list)

        # Only proceed if all PK attributes from other table are present in current columns
        if pk_set.issubset(set(current_columns)):
            # Map each PK attribute to FK column in current table using heuristics
            for pk_attr in pk_list:
                for col in current_columns:
                    if (
                        col.lower() == pk_attr.lower()
                        or col.lower().endswith(pk_attr.lower())
                        or pk_attr.lower() in col.lower()
                        or (
                            col.lower().endswith("_id")
                            and pk_attr.lower() in col.lower()
                        )
                    ):
                        # Record FK column referencing other table's PK column
                        foreign_keys[col] = {
                            "ref_table": other_table,
                            "ref_column": pk_attr,
                        }
    return foreign_keys
