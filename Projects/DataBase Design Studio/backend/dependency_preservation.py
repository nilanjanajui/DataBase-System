from typing import List, Set, Tuple, FrozenSet
from fd_modified import closure, project_fds_on_schema, minimize_fds

FD = Tuple[FrozenSet[str], FrozenSet[str]]


def normalize_fd_attrs(fd: FD) -> FD:
    """Normalize attribute names in functional dependencies."""
    normalize = lambda s: frozenset(
        attr.strip().rstrip(".").lower().replace(" ", "_") for attr in s
    )
    lhs, rhs = fd
    return (normalize(lhs), normalize(rhs))


def normalize_fds(fds: List[FD]) -> List[FD]:
    """Normalize all functional dependencies in the list."""
    return [normalize_fd_attrs(fd) for fd in fds]


def check_dependency_preservation(
    original_fds: List[FD], decomposed_schemas: List[Set[str]], decomposed_fds: List[FD]
) -> bool:
    """
    Check if all original FDs can be derived from the decomposed FDs.

    Args:
        original_fds: List of original functional dependencies
        decomposed_schemas: List of attribute sets in each decomposed table
        decomposed_fds: List of functional dependencies in the decomposition

    Returns:
        bool: True if all dependencies are preserved, False otherwise
    """
    # Normalize and minimize both sets of FDs
    original_fds_norm = normalize_fds(minimize_fds(original_fds))
    decomposed_fds_norm = normalize_fds(minimize_fds(decomposed_fds))

    # Check each original FD
    for lhs, rhs in original_fds_norm:
        closure_of_lhs = closure(set(lhs), decomposed_fds_norm)
        if not rhs.issubset(closure_of_lhs):
            # Try cross-schema check before giving up
            if not _check_cross_schema_fd(
                (lhs, rhs), original_fds_norm, decomposed_schemas
            ):
                return False
    return True


def _check_cross_schema_fd(
    fd: FD, original_fds: List[FD], schemas: List[Set[str]]
) -> bool:
    """
    Check if an FD can be derived from attributes across multiple schemas.

    Args:
        fd: The functional dependency to check
        original_fds: List of all original FDs
        schemas: List of attribute sets in each decomposed table

    Returns:
        bool: True if the FD can be derived across schemas
    """
    lhs, rhs = fd

    # Find all schemas relevant to this FD
    relevant_schemas = [s for s in schemas if lhs.intersection(s)]

    # If no schemas contain any part of LHS, FD can't be preserved
    if not relevant_schemas:
        return False

    # Initialize closure with LHS attributes
    closure_result = set(lhs)
    changed = True

    # Compute closure across schemas
    while changed:
        changed = False
        for schema in relevant_schemas:
            # Get FDs that can be projected on this schema
            schema_fds = [
                (l, r)
                for l, r in original_fds
                if l.issubset(schema) and r.issubset(schema)
            ]

            # Compute closure within this schema
            schema_closure = closure(closure_result.intersection(schema), schema_fds)

            # Update overall closure
            new_result = closure_result.union(schema_closure)
            if new_result != closure_result:
                closure_result = new_result
                changed = True
                if rhs.issubset(closure_result):
                    return True

    return rhs.issubset(closure_result)


def is_dependency_preserved(
    original_fds: List[FD], decomposed_schemas: List[Set[str]]
) -> bool:
    """
    High-level function to check dependency preservation for given schemas.
    Projects original FDs onto each schema and combines them before checking.

    Args:
        original_fds: List of original functional dependencies
        decomposed_schemas: List of attribute sets in each decomposed table

    Returns:
        bool: True if dependencies are preserved, False otherwise
    """
    # Minimize original FDs once
    minimized_original = minimize_fds(original_fds)

    # Project onto each decomposed schema and combine all projected FDs
    combined_projected_fds = []
    for schema in decomposed_schemas:
        projected = project_fds_on_schema(minimized_original, schema)
        combined_projected_fds.extend(projected)

    # Minimize the combined projected FDs to avoid duplicates/redundancy
    minimized_projected = minimize_fds(combined_projected_fds)

    # Check preservation with enhanced algorithm
    return check_dependency_preservation(
        original_fds, decomposed_schemas, minimized_projected
    )


def get_lost_dependencies(
    original_fds: List[FD], decomposed_schemas: List[Set[str]]
) -> List[FD]:
    """
    Identify which dependencies are lost during decomposition.

    Args:
        original_fds: List of original functional dependencies
        decomposed_schemas: List of attribute sets in each decomposed table

    Returns:
        List[FD]: List of dependencies that were not preserved
    """
    minimized_original = minimize_fds(original_fds)
    lost_fds = []

    # Project onto each decomposed schema and combine all projected FDs
    combined_projected_fds = []
    for schema in decomposed_schemas:
        projected = project_fds_on_schema(minimized_original, schema)
        combined_projected_fds.extend(projected)

    minimized_projected = minimize_fds(combined_projected_fds)

    # Check each original FD
    for fd in minimized_original:
        lhs, rhs = fd
        closure_of_lhs = closure(set(lhs), minimized_projected)
        if not rhs.issubset(closure_of_lhs):
            if not _check_cross_schema_fd(fd, minimized_original, decomposed_schemas):
                lost_fds.append(fd)

    return lost_fds
