#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BAM_to_seqdepcov v0.1.5

Author: Vanness Mach (Bear)

Purpose:
    Generate per-base sequencing depth from a BAM file using samtools.

Method:
    samtools depth -a -q 0 -Q 0

    -a        : include all positions, even zero-depth
    -q 0      : no mapping quality filter (keep all reads)
    -Q 0      : no base quality filter (keep all bases)

Output:
    <prefix>.depth.txt

Usage:
    python BAM_to_seqdepcovv0.1.5.py input.bam [output_prefix]

    If output_prefix is not provided, the BAM filename stem is used.

Notes:
    Input BAM must be coordinate-sorted.
    To sort: samtools sort -o sorted.bam input.bam
    To index: samtools index sorted.bam

Changes from v0.1.0:
    - Version synchronised with seqdepcov_plot v0.1.5
    - Expanded docstring and usage notes
"""

__version__ = "0.1.5"

import argparse
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Generate per-base sequencing depth from BAM using samtools."
    )
    parser.add_argument(
        "bam",
        help="Input BAM file (coordinate-sorted)"
    )
    parser.add_argument(
        "prefix",
        nargs="?",
        help="Output prefix (default: BAM filename without extension)"
    )
    args = parser.parse_args()

    bam_path = Path(args.bam)
    if not bam_path.exists():
        sys.exit(f"ERROR: BAM file not found: {bam_path}")

    prefix   = args.prefix if args.prefix else bam_path.stem
    out_file = f"{prefix}.depth.txt"

    cmd = [
        "samtools", "depth",
        "-a", "-q", "0", "-Q", "0",
        str(bam_path)
    ]

    print(">>> Generating per-base sequencing depth")
    print(">>> Command:", " ".join(cmd))

    with open(out_file, "w") as out:
        proc = subprocess.Popen(cmd, stdout=out, stderr=subprocess.PIPE, text=True)
        _, err = proc.communicate()

    if proc.returncode != 0:
        sys.exit(f"ERROR running samtools depth:\n{err}")

    print("====================================")
    print("Depth file generated successfully")
    print(f"Version     : {__version__}")
    print(f"Input BAM   : {bam_path}")
    print(f"Output file : {out_file}")
    print("====================================")


if __name__ == "__main__":
    main()
