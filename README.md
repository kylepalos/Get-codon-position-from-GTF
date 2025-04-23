# Get-codon-position-from-GTF

I may be reinventing the wheel or not taking the optimal approach but sometimes I want to associate specific genomic position (e.g., splice-sites or RNA methlyation sites) with their codon position (i.e., first, second, third or A/P/E site.)

I couldn't find a great way to do this en-masse for hundreds/thousands of sites at a time (i.e., in preparation for bedtools intersect.)

This python script takes your GTF file, for example:

```
1	araport11	CDS	3760	3913	.	+	0	transcript_id "transcript:AT1G01010.1"; gene_id "gene:AT1G01010";
```

and outputs:

```
1	3759	3760	pos1-transcript:AT1G01010.1	0	+
1	3760	3761	pos2-transcript:AT1G01010.1	0	+
1	3761	3762	pos3-transcript:AT1G01010.1	0	+
.
.
.
```

I did a lot of spot checking and it appears to handle splicing and negative strand transcripts properly.

Just run:

```
python get_codon_position_from_GTF.py super_cool.gtf codon_positions.bed
```

Be aware that your output is likely to be large - every CDS nucleotide position will end up in the bed file.

My GTF with 286,067 CDS lines made a 3.2GB output bed file.
