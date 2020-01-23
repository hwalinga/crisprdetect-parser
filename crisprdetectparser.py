#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parser for CRISPRDetect output files.

Run with --help for an how to run.

Minimum Python version is 3.6.

Hielke Walinga (hielkewalinga@gmail.com)
"""
import argparse
import fileinput
import os
import re
import sys
from collections import defaultdict
from itertools import takewhile
from os import path
from typing import Dict

header = (
    "genome\tcontig\tarray_id\tbegin\tend\torientation\tnumber_of_spacers\t"
    "array_family\tquality_score\trepeat_sequence"
)

ap = argparse.ArgumentParser(
    prog="CRISPRDetect parser",
    description="Run this progrom on CRISPRDetect output files to extract"
    " the spacers and the metadate about the CRISPR arrays."
    " The program can process the CRISPR array files with sufficient quality score"
    " (with the .crisprdetect extension), but also the array files with"
    " a score below the required quality score (with the .crisprdetect.fp extension)",
)
ap.add_argument("files", nargs="*", help="All the .crisprdetect(.fp) output files.")
ap.add_argument(
    "--spacers-directory",
    nargs="?",
    const="spacers_dir",
    default=None,
    help="Create spacers folder. Creates a folder with fasta files that contain the"
    " spacer sequences for each genome."
    " Leave out if you don't want to extract the spacers.",
)
ap.add_argument(
    "--out",
    type=argparse.FileType("a+"),
    default=sys.stdout,
    help="Output file, if left out, this will be stdout. If file already exist"
    " it will append.",
)
ap.add_argument(
    "--sep", default="\t", help="Seperator in the metadata file. (Default: tab)"
)
ap.add_argument(
    "--crisprdetect-extension",
    default="crisprdetect",
    help="Extension of crisperdetect files that is cut-off for genome name."
    " (Default: crisprdetect)",
)
ap.add_argument(
    "--spacers-extension",
    default="spacers.fna",
    help="Extension string of the spacers fasta file. (Default: spacers.fna)",
)
ap.add_argument(
    "--header", action="store_true", help=f"Output file with a header: {header}"
)
ap.add_argument("--force", action="store_true", help="Overwrite existing files.")
args = ap.parse_args()


if args.spacers_directory:
    if not path.isdir(args.spacers_directory):
        os.mkdir(args.spacers_directory)
    spacers_file = None

if args.header:
    print(header, file=args.out)

contigs_counter: Dict[str, int] = defaultdict(int)

with fileinput.input(args.files) as f:
    for line in f:

        if f.isfirstline():  # Initialize for new file, new genome.
            genome = path.basename(f.filename()).replace(
                f".{args.crisprdetect_extension}", ""
            )

            contigs_counter.clear()

            if args.spacers_directory:
                if spacers_file:
                    spacers_file.close()
                spacers_file_name = f"{genome}.{args.spacers_extension}"
                spacers_path_name = path.join(args.spacers_directory, spacers_file_name)
                if not args.force and path.exists(spacers_path_name):
                    raise Exception(
                        f"{spacers_path_name} already exists."
                        " Set --force to overwrite this file,"
                        " and other already existing files."
                    )
                spacers_file = open(spacers_path_name, "w")

        # Array definition starts now.
        if line.startswith(">"):
            F = line.split()
            orientation = F[-1].strip()
            contig = F[0].lstrip(">")
            contigs_counter[contig] += 1
            number = contigs_counter[contig]
            array_id = f"{contig}_{number}"

            # Loop untill spacers list.
            all(takewhile(lambda l: not str(l).startswith("==="), f))

            # Loop over all spacers.
            for idx, line in enumerate(f):
                F = line.split()
                spacer_sequence = F[5]

                if spacer_sequence == "|":  # End of spacers list.
                    end = int(F[0]) + (1 if orientation == "Forward" else -1) * int(
                        F[1]
                    )
                    num_spacers = idx

                    next(f)
                    line = next(f)
                    repeat = line.split()[4]
                    break

                if idx == 0:
                    begin = int(F[0])

                if args.spacers_directory:
                    print(f">{array_id}_{idx + 1}", file=spacers_file)
                    print(spacer_sequence, file=spacers_file)

            # Continue till Array family, and output array, and continue main loop.
            for line in f:

                if line.startswith("# Questionable array :"):
                    score = line.split(": ")[-1].strip()

                if line.startswith("# Array family :"):
                    family = re.search(r"# Array family :\s(.*?)(?:\s|$)", line)[1]
                    if orientation != "Forward":
                        begin, end = end, begin
                    print(
                        genome,
                        contig,
                        array_id,
                        begin,
                        end,
                        orientation,
                        num_spacers,
                        family,
                        score,
                        repeat,
                        sep=args.sep,
                        file=args.out,
                    )
                    break
