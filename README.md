# Get-codon-position-from-GTF

I may be reinventing the wheel or not taking the optimal approach but sometimes I want to associate a specific genomic position (e.g., DNA or RNA methlyation site) with the codon position (i.e., first, second, third or A/P/E site.)

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

I did a lot of spot checking but it appears to handle splicing and negative strand transcripts properly.

Just run:

```
python super_cool.gtf hopefully_correct_codon_positions.bed
```
