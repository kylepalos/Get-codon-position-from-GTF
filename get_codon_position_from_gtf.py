#!/usr/bin/env python3
import csv
import re
import argparse


# define the conversion function
def gtf_to_codon_positions_bed(gtf_file, output_bed_file):
    # Group CDS features by transcript ID
    transcript_cds = {}
    
    with open(gtf_file, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            
            fields = line.strip().split('\t')
            if len(fields) < 9 or fields[2] != 'CDS':
                continue
            
            # define what the fields are
            
            chrom = fields[0]
            start = int(fields[3])  # 1-based in GTF
            end = int(fields[4])    # 1-based inclusive in GTF
            strand = fields[6]
            frame = int(fields[7])
            
            # extract transcript ID using regex
            match = re.search(r'transcript_id "([^"]+)"', fields[8])
            if not match:
                continue
            transcript_id = match.group(1)
            
            # associate transcript IDs with their specific CDS
            if transcript_id not in transcript_cds:
                transcript_cds[transcript_id] = []
            
            transcript_cds[transcript_id].append((chrom, start, end, strand, frame))
    
    with open(output_bed_file, 'w') as out:
        for transcript_id, cds_list in transcript_cds.items():
            # get the strand from the first CDS feature
            strand = cds_list[0][3]
            
            # properly handle strand info for each CDS
            if strand == '+':
                cds_list.sort(key=lambda x: x[1])  # Sort by start position for + strand
            else:
                cds_list.sort(key=lambda x: x[1], reverse=True)  # Sort in reverse for - strand
            
            # Initialize codon position counter
            current_codon_pos = 0  # Will be set based on first CDS frame
            
            # Process all CDS features for this transcript
            for i, (chrom, start, end, strand, frame) in enumerate(cds_list):
                # Set initial codon position for the first CDS based on frame
                if i == 0:
                    if strand == '+':
                        # For positive strand: frame 0 → pos1, frame 1 → pos2, frame 2 → pos3
                        current_codon_pos = frame + 1
                    else:
                        # For negative strand: frame 0 → pos1, frame 1 → pos3, frame 2 → pos2
                        if frame == 0:
                            current_codon_pos = 1
                        elif frame == 1:
                            current_codon_pos = 3
                        else:  # frame == 2
                            current_codon_pos = 2
                
                # Process each nucleotide in this CDS
                if strand == '+':
                    # Process positions from start to end for + strand
                    for pos in range(start, end + 1):
                        bed_start = pos - 1  # Convert to 0-based for BED
                        bed_end = pos        # BED end is exclusive
                        
                        # Write BED line
                        out.write(f"{chrom}\t{bed_start}\t{bed_end}\tpos{current_codon_pos}-{transcript_id}\t0\t{strand}\n")
                        
                        # Update codon position for next nucleotide (cycle 1→2→3→1...)
                        current_codon_pos = current_codon_pos % 3 + 1
                else:
                    # Process positions from end to start for - strand (reverse direction)
                    for pos in range(end, start - 1, -1):
                        bed_start = pos - 1  # Convert to 0-based for BED
                        bed_end = pos        # BED end is exclusive
                        
                        # Write BED line
                        out.write(f"{chrom}\t{bed_start}\t{bed_end}\tpos{current_codon_pos}-{transcript_id}\t0\t{strand}\n")
                        
                        # Update codon position for next nucleotide (cycle 1→2→3→1...)
                        current_codon_pos = current_codon_pos % 3 + 1

# process command line arguments
def main():
    parser = argparse.ArgumentParser(description='Convert GTF to codon position BED file')
    parser.add_argument('input_gtf', help='Input GTF file')
    parser.add_argument('output_bed', help='Output BED file')
    args = parser.parse_args()
    
    gtf_to_codon_positions_bed(args.input_gtf, args.output_bed)
    print(f"Converted {args.input_gtf} to codon position BED file: {args.output_bed}")

if __name__ == "__main__":
    main()