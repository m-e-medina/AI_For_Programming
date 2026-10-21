"""Print GC percentages for records in a FASTA file."""

import argparse
import sys


def read_fasta_records(path):
    """Yield (header, sequence) pairs from a FASTA file."""
    header = None
    sequence = []

    with open(path, encoding="utf-8") as fasta:
        for line_number, line in enumerate(fasta, start=1):
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    yield header, "".join(sequence)
                header = line[1:]
                sequence = []
            elif header is None:
                raise ValueError(
                    f"Sequence found before FASTA header on line {line_number}"
                )
            else:
                sequence.append(line)

    if header is not None:
        yield header, "".join(sequence)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fasta_file", help="input FASTA file")
    parser.add_argument(
        "--min-gc",
        type=float,
        default=None,
        metavar="FLOAT",
        help="print only records with GC content above this percentage",
    )
    args = parser.parse_args()

    if args.min_gc is not None and not 0 <= args.min_gc <= 100:
        parser.error("--min-gc must be between 0 and 100")

    for header, sequence in read_fasta_records(args.fasta_file):
        if not sequence:
            print(f"Warning: skipping empty sequence for {header!r}", file=sys.stderr)
            continue
        gc_percent = (sequence.upper().count("G") + sequence.upper().count("C")) / len(
            sequence
        ) * 100
        if args.min_gc is None or gc_percent > args.min_gc:
            print(f"{header}\t{gc_percent:.4f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())

