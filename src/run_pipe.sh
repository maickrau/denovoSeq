#!/usr/bin/sh

# input: child_reads.fa, mat_reads.fa, pat_reads.fa

grep '>' < child_reads.fa | tr -d '>' > child_readnames.txt
grep '>' < mat_reads.fa | tr -d '>' > mat_readnames.txt
grep '>' < pat_reads.fa | tr -d '>' > pat_readnames.txt

/usr/bin/time -v MBG -t 4 -k 1001 -r 15000 -R 4000 -w 100 --kmer-abundance 1 --unitig-abundance 2 --error-masking=msat --output-sequence-paths paths.gaf --hpc-variant-onecopy-coverage 25 --do-unsafe-guesswork-resolutions --out hifi-resolved.gfa -i mat_reads.fa -i pat_reads.fa -i child_reads.fa 1> stdout_mbg.txt 2> stderr_mbg.txt

awk '$1=="S"{print "S\t" $2 "\t*\tLN:i:" length($3) "\t" $4 "\t" $5;}$1!="S"{print;}' < hifi-resolved.gfa > noseq-hifi-resolved.gfa
./color_graph.py child_readnames.txt mat_readnames.txt pat_readnames.txt < paths.gaf > color.csv

grep ",hap1," < color.csv | cut -d ',' -f 1 > all_novel_seq.txt
./get_confident_novel_sequences.py color.csv < noseq-hifi-resolved.gfa > confident_novel_seq.txt

./get_reads_in_node_sets.py confident_novel_seq.txt < paths.gaf > probably_de_novo_info.txt
./get_reads_in_node_sets.py all_novel_seq.txt < paths.gaf > potentially_de_novo_info.txt
