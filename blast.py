import os
import glob
from global_param import *

class blast_clean(object):
    def __init__(self, target_folder, filetypes):
        self.target_folder = target_folder
        self.filetypes = filetypes
    def clean_folder(self):
        for ft in self.filetypes:
            for to_remove in glob.glob("{}{}".format(self.target_folder, ft)):
                os.remove(to_remove)

def blast_anti_crispr_gendb():
    cmd = "{} -in {} -out {} -dbtype prot".format(MAKEBLASTDB_PATH, ACR_PROT_PATH, ACR_PROT_BLASTDB)
    os.system(cmd)

def blast_aca_gendb():
    cmd = "{} -in {} -out {} -dbtype prot".format(MAKEBLASTDB_PATH, ACA_PROT_PATH, ACA_PROT_BLASTDB)
    os.system(cmd)

def blast_anti_crispr_run(domains, subset=999999):
    for domain in domains:
        subset_count = 0
        for filename in os.listdir(domain):
            if filename.endswith(".faa.gz"):
                filename_out = filename.replace('.faa.gz', '.out')
                filename_filtered = filename.replace('.faa.gz', '.filtered')
                if os.path.exists(filename_filtered):
                    continue
                cmd = "zcat {}{} " \
                      "| {} -db {} -out {}{} -num_threads {} " \
                      "-outfmt \"6 qseqid sseqid qlen slen length pident gapopen evalue\" " \
                      "-evalue 0.01".format(
                    domain, filename,
                    BLASTP_PATH, ACR_PROT_BLASTDB,
                    BLAST_ACR_OUT, filename_out,
                    NUMBER_OF_THREADS)
                os.system(cmd)
                cmd = "awk -F '\t' '{{ if (($6>70) && ($3*0.7<$5)) {{print}} }}' {}{} | awk '!seen[$3]++' >> {}{}".format(
                    BLAST_ACR_OUT, filename_out,
                    BLAST_ACR_OUT, filename_filtered)
                os.system(cmd)
                os.remove("{}{}".format(BLAST_ACR_OUT, filename_out))
            subset_count+=1
            if subset == subset_count:
                break

def blast_aca_run(domains, subset=999999):
    for domain in domains:
        subset_count=0
        for filename in os.listdir(domain):
            if filename.endswith(".faa.gz"):
                filename_out = filename.replace('.faa.gz', '.out')
                filename_filtered = filename.replace('.faa.gz', '.filtered')
                if os.path.exists(filename_filtered):
                    continue
                cmd = "zcat {}{} " \
                      "| {} -db {} -out {}{} -num_threads {} " \
                      "-outfmt \"6 qseqid sseqid qlen slen length pident gapopen evalue\" " \
                      "-evalue 0.01".format(
                    domain, filename,
                    BLASTP_PATH, ACA_PROT_BLASTDB,
                    BLAST_ACA_OUT, filename_out,
                    NUMBER_OF_THREADS)
                os.system(cmd)
                cmd = "awk -F '\t' '{{ if (($6>70) && ($3*0.7<$5)) {{print}} }}' {}{} | awk '!seen[$3]++' >> {}{}".format(
                    BLAST_ACA_OUT, filename_out,
                    BLAST_ACA_OUT, filename_filtered)
                os.system(cmd)
                os.remove("{}{}".format(BLAST_ACA_OUT, filename_out))
            subset_count += 1
            if subset == subset_count:
                break