import sys


def reformat_rdp(input_file, output_file):
    """
    Reformat RDP classifier output into a QIIME2-compatible taxonomy format.

    Args:
        input_file (str): Path to the RDP classifier output file.
        output_file (str): Path to save the reformatted output.
    """
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # Write header for QIIME2-compatible taxonomy file
        outfile.write("Sequence ID\tTaxonomy\tConfidence\n")

        for line in infile:
            # Split the line into fields
            fields = line.strip().split('\t')

            if len(fields) < 2:
                continue  # Skip malformed lines

            seq_id = fields[0]  # First column is the sequence ID

            # Parse taxonomy and confidence scores
            taxonomy = []
            confidence = None
            for i in range(2, len(fields), 3):  # Taxonomy is every third column starting at index 2
                if i + 1 < len(fields):
                    taxon = fields[i]
                    rank = fields[i + 1]
                    conf = fields[i + 2]

                    # Add taxon if it exists and has a valid rank
                    if taxon and rank:
                        taxonomy.append(taxon)

                    # Update confidence score to the last valid value
                    confidence = conf

            # Combine taxonomy levels into a semicolon-separated string
            taxonomy_str = ';'.join(taxonomy)

            # Write reformatted line
            outfile.write(f"{seq_id}\t{taxonomy_str}\t{confidence}\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python reformat_rdp_output.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    reformat_rdp(input_file, output_file)
    print(f"Reformatted file saved to: {output_file}")
