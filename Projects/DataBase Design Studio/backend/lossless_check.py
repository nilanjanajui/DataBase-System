from typing import List, Set, Tuple, FrozenSet

# Type alias for a Functional Dependency: (LHS, RHS)
FD = Tuple[FrozenSet[str], FrozenSet[str]]


def is_lossless_decomposition(
    original_attrs: Set[str], decomposed_schemas: List[Set[str]], fds: List[FD]
) -> bool:
    """
    Determines whether the decomposition is lossless using the Chase algorithm.

    Args:
        original_attrs (Set[str]): Set of all attributes in the original relation.
        decomposed_schemas (List[Set[str]]): List of sets, each representing attributes in a decomposed schema.
        fds (List[FD]): List of functional dependencies, each as (LHS, RHS) where both are frozen sets.

    Returns:
        bool: True if the decomposition is lossless, False otherwise.
    """
    if not original_attrs or not decomposed_schemas or not fds:
        print("Lossless Check Error: Missing inputs (attributes/schemas/fds)")
        return False

    # Initialize tableau: { attribute : set of symbols (a_i or b_i_attr) }
    tableau = {attr: set() for attr in original_attrs}
    for i, schema in enumerate(decomposed_schemas):
        for attr in original_attrs:
            if attr in schema:
                tableau[attr].add(f"a{i}")
            else:
                tableau[attr].add(f"b{i}_{attr}")

    # Debug: Initial tableau
    print("\nInitial Tableau:")
    for attr in tableau:
        print(f"  {attr}: {tableau[attr]}")

    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if not lhs:
                continue

            try:
                # Common values across all tableau rows for LHS attributes
                common_rows = set.intersection(*[tableau[attr] for attr in lhs])
            except KeyError as e:
                print(f"Attribute {e} in FD LHS not found in tableau")
                continue

            for attr in rhs:
                if attr not in tableau:
                    continue
                before = tableau[attr].copy()
                tableau[attr].update(common_rows)
                if tableau[attr] != before:
                    changed = True

    # Debug: Final tableau
    print("\nFinal Tableau After Chase:")
    for attr in tableau:
        print(f"  {attr}: {tableau[attr]}")

    # Lossless if any a_i appears in all rows
    for i in range(len(decomposed_schemas)):
        if all(f"a{i}" in tableau[attr] for attr in original_attrs):
            print(f"\nLossless decomposition confirmed via row a{i}.")
            return True

    print("\nLossless decomposition FAILED.")
    return False
