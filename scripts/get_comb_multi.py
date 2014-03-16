#! /usr/bin/env python
"""
Count the median/avg k-mer abundance for each sequence in the input file,
based on the k-mer counts in the given counting hash.  Can be used to
estimate expression levels (mRNAseq) or coverage (genomic/metagenomic).

% scripts/count-median.py <htname> <output> <input seqs> 

Use '-h' for parameter help.

The output file contains sequence id, median, average, stddev, and seq length.

NOTE: All 'N's in the input sequences are converted to 'G's.
# config files:
# htfile1 htfile2 htfile3 htfile4 etc.
# seqfile1 seqfile2 seqfile3 seqfile4 etc.
# 1000000000

"""
import sys, screed, os
import khmer
import argparse

###

def main():
    parser = argparse.ArgumentParser(description='Get coverage of sequences in multiple samples')

    parser.add_argument('config_file')

    args = parser.parse_args()

    file_config = args.config_file

    f_config = open(file_config, 'r')
    lines = f_config.readlines()
    f_config.close()
    print lines
    htfiles = lines[0].split()
    filenames = lines[1].split()
    mem_size = int(lines[2])
    
    round_size = 0
    all_ht = []
    round_ht = []
    for htfile in htfiles:
        size = os.path.getsize(htfile)
        print round_size
        if round_size + size < mem_size:
            round_size = round_size + size
            round_ht.append(htfile)
        else:
            all_ht.append(round_ht)
            round_size = size
            round_ht = []
            round_ht.append(htfile)
    all_ht.append(round_ht)
    print all_ht
    
    for round in range(len(all_ht)): # deal with the ht in memory
        htfiles = all_ht[round]
        hts = []
        for htfile in htfiles:
            print 'loading counting hash from', htfile
            ht = khmer.load_counting_hash(htfile)
            K = ht.ksize()
            hts.append(ht)
            
        for n, input_filename in enumerate(filenames):
            if round >0:
                os.rename(input_filename+'.comb', input_filename+'.temp')
                temp_old = open(input_filename+'temp_old','r')
            output = open(input_filename+'.comb','w')
            print 'consuming input', input_filename
            for record in screed.open(input_filename):
                seq = record.sequence.upper()
                if 'N' in seq:
                    seq = seq.replace('N', 'G')
                if round == 0:
                    to_print = record.name
                else:
                    to_print = temp_old.readline()
                    
                if K <= len(seq):
                    for ht in hts:
                        med, _, _ = ht.get_median_count(seq)
                        to_print = to_print + ' '+str(med)
                        
                    print >>output, to_print



if __name__ == '__main__':
    main()
