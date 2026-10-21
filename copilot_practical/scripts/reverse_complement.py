# reverse_complement.py
# Reads a single-line DNA sequence from a FASTA file and prints its
# reverse complement.

COMPLEMENT = {"A": "T", "T": "A", "C": "G", "G": "C"}

def read_fasta_sequence(path):
    """Return the sequence (str) from a single-record FASTA file."""
    sequence = []
    header_seen = False
    with open(path, encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header_seen:
                    raise ValueError("Expected a single-record FASTA file")
                header_seen = True
            elif not header_seen:
                raise ValueError(
                    f"Sequence found before FASTA header on line {line_number}"
                )
            else:
                sequence.append(line)

    if not header_seen:
        raise ValueError("Missing FASTA header")
    return "".join(sequence)

def reverse_complement(seq):
    """Return the reverse complement of a DNA sequence."""
    try:
        return "".join(COMPLEMENT[base] for base in reversed(seq))
    except KeyError as error:
        raise ValueError(
            f"Invalid DNA character {error.args[0]!r}; expected only A, T, C, or G"
        ) from None

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <fasta-file>", file=sys.stderr)
        sys.exit(2)
    seq = read_fasta_sequence(sys.argv[1])
    print(reverse_complement(seq))
