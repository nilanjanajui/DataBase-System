import pandas as pd
from typing import List, Set, Tuple, Dict, FrozenSet
from collections import defaultdict
from itertools import combinations
from cleanModify import normalize_columns


# Type alias for a Functional Dependency
FD = Tuple[FrozenSet[str], FrozenSet[str]]


def detect_functional_dependencies(
    df: pd.DataFrame,
    max_comb_size: int = 3,
    rhs_cardinality_threshold: int = 100,
    verbose: bool = True,
) -> List[FD]:
    """
    Detect FDs by checking if combinations of columns (up to max_comb_size) determine others.
    Skips high-cardinality RHS if threshold is exceeded.
    """

    df.columns = normalize_columns(df.columns)

    fds: List[FD] = []
    columns = df.columns.tolist()

    for col_b in columns:
        # Skip high-cardinality RHS
        if df[col_b].nunique(dropna=False) > rhs_cardinality_threshold:
            if verbose:
                print(f"Skipping RHS column due to high cardinality: {col_b}")
            continue

        found_fd = False
        for size in range(1, max_comb_size + 1):
            for lhs_attrs in combinations(columns, size):
                if col_b in lhs_attrs:
                    continue  # Skip trivial or invalid combinations

                grouped = df.groupby(list(lhs_attrs), dropna=False)[col_b].nunique(
                    dropna=False
                )

                if grouped.empty:
                    continue

                if all(grouped == 1):
                    fds.append((frozenset(lhs_attrs), frozenset([col_b])))
                    found_fd = True
                    if verbose:
                        print(f"FD found: {set(lhs_attrs)} -> {col_b}")
                    break  # Minimal FD found

            if found_fd:
                break

        if not found_fd and verbose:
            print(f"No FD found for column: {col_b}")

    return fds


def closure(attributes: Set[str], fds: List[FD]) -> Set[str]:
    """
    Compute attribute closure for a given set of attributes using provided FDs.
    """
    result = set(attributes)
    while True:
        added = False
        for lhs, rhs in fds:
            if lhs.issubset(result) and not rhs.issubset(result):
                result.update(rhs)
                added = True
        if not added:
            break
    return result


def expand_rhs_to_singletons(fds: List[FD]) -> List[FD]:
    """
    Ensure all FDs are of the form X → A (singleton RHS).
    """
    return [(lhs, frozenset([attr])) for lhs, rhs in fds for attr in rhs]


def remove_extraneous_lhs(fds: List[FD]) -> List[FD]:
    """
    Remove unnecessary attributes from LHS of each FD.
    """
    result = []
    for lhs, rhs in fds:
        lhs_set = set(lhs)
        for attr in list(lhs_set):
            test_lhs = lhs_set - {attr}
            if not test_lhs:
                continue
            temp_fds = [fd for fd in fds if fd != (frozenset(lhs_set), rhs)]
            temp_fds.append((frozenset(test_lhs), rhs))
            if rhs.issubset(closure(test_lhs, temp_fds)):
                lhs_set.remove(attr)
        result.append((frozenset(lhs_set), rhs))
    return result


def remove_redundant_fds(fds: List[FD]) -> List[FD]:
    """
    Remove redundant FDs by checking if RHS can be derived from others.
    """
    result = []
    for i, (lhs, rhs) in enumerate(fds):
        remaining = fds[:i] + fds[i + 1 :]
        if not rhs.issubset(closure(set(lhs), remaining)):
            result.append((lhs, rhs))
    return result


def minimize_fds(fds: List[FD]) -> List[FD]:
    """
    Return the minimal cover of the given FDs.
    """
    step1 = expand_rhs_to_singletons(fds)
    step2 = remove_extraneous_lhs(step1)
    step3 = remove_redundant_fds(step2)
    return step3


def group_fds(fds: List[FD]) -> Dict[FrozenSet[str], Set[str]]:
    """
    Group minimized FDs into dict: LHS → set of RHS attributes.
    """
    fd_dict: Dict[FrozenSet[str], Set[str]] = defaultdict(set)
    for lhs, rhs in fds:
        fd_dict[lhs].update(rhs)
    return dict(fd_dict)


def project_fds_on_schema(fds: List[FD], schema: Set[str]) -> List[FD]:
    """
    Return FDs applicable to a subset of attributes (schema).
    """
    return [
        (lhs, rhs) for lhs, rhs in fds if lhs.issubset(schema) and rhs.issubset(schema)
    ]


def attr_closure_d(
    attributes: Set[str], fds: List[FD], relations: List[Set[str]]
) -> Set[str]:
    """
    Dependency preservation test used in decomposition.
    """
    result = set(attributes)
    changed = True
    while changed:
        changed = False
        for rel in relations:
            relevant_fds = project_fds_on_schema(fds, rel)
            sub_attrs = result & rel
            expanded = closure(sub_attrs, relevant_fds) & rel
            new_result = result | expanded
            if new_result != result:
                result = new_result
                changed = True
    return result
