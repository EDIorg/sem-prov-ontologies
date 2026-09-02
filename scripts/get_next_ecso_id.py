#!/usr/bin/env python3
"""
Dynamic ID Discovery Utility for ECSO Ontology.

Scans ecso/ECSO8.owl for allocated owl:Class IDs matching the standard
8-digit numeric CURIE pattern (http://purl.dataone.org/odo/ECSO_XXXXXXXX)
and calculates the next available sequential ID(s).
"""

import argparse
import os
import re
import sys

BASE_URI = "http://purl.dataone.org/odo/ECSO_"
DEFAULT_OWL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "ecso",
    "ECSO8.owl",
)


def get_allocated_class_ids(owl_path: str) -> list[int]:
    """Extract all allocated 8-digit numeric class IDs from the OWL file."""
    if not os.path.isfile(owl_path):
        print(f"Error: OWL file not found at '{owl_path}'", file=sys.stderr)
        sys.exit(1)

    with open(owl_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Specifically match owl:Class rdf:about="...ECSO_(\d{8})..."
    # to avoid capturing legacy non-class annotation properties (like ECSO_01000005)
    class_pattern = r"<owl:Class\s+rdf:about=[\"\x27].*?ECSO_(\d{8})[\"\x27]"
    matches = [int(m) for m in re.findall(class_pattern, content)]

    if not matches:
        # Fallback to general URI pattern if needed
        general_pattern = r"http://purl\.dataone\.org/odo/ECSO_(\d{8})"
        matches = [int(m) for m in re.findall(general_pattern, content)]

    return sorted(list(set(matches)))


def main():
    parser = argparse.ArgumentParser(
        description="Discover next available sequential ECSO class ID(s)."
    )
    parser.add_argument(
        "--owl-file",
        default=DEFAULT_OWL_PATH,
        help=f"Path to ECSO OWL file (default: {DEFAULT_OWL_PATH})",
    )
    parser.add_argument(
        "--count",
        "-n",
        type=int,
        default=1,
        help="Number of sequential IDs to allocate (default: 1)",
    )
    parser.add_argument(
        "--curie-only",
        action="store_true",
        help="Output only the CURIE (e.g. ECSO:00010137)",
    )
    parser.add_argument(
        "--uri-only",
        action="store_true",
        help="Output only the full URI (e.g. http://purl.dataone.org/odo/ECSO_00010137)",
    )

    args = parser.parse_args()

    allocated_ids = get_allocated_class_ids(args.owl_file)
    if not allocated_ids:
        print("Error: No allocated ECSO IDs discovered.", file=sys.stderr)
        sys.exit(1)

    max_id = max(allocated_ids)
    next_ids = [max_id + i for i in range(1, args.count + 1)]

    for id_num in next_ids:
        curie = f"ECSO:{id_num:08d}"
        uri = f"{BASE_URI}{id_num:08d}"

        if args.curie_only:
            print(curie)
        elif args.uri_only:
            print(uri)
        else:
            print(f"{curie} ({uri})")


if __name__ == "__main__":
    main()
