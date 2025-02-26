file = '../../fastqc_v0.12.1/FastQC/Configuration/limits.txt'
with open(file) as f:
    for line in f:
        if line.startswith('kmer'):
            print(line)