import os
import glob
import global_param

BLAST_PATH = "blast/"
MAKEBLASTDB_PATH = "utils/blast/ncbi-blast-2.7.1+/bin/makeblastdb"
BLASTP_PATH = "utils/blast/ncbi-blast-2.7.1+/bin/blastp"
ACR_PROT_PATH = "download_acrdb/proteinSequence.faa"
ACA_PROT_PATH = "aca_seqs/acaSequences.faa"
ACR_PROT_BLASTDB = "blast/acrdb_db"
ACA_PROT_BLASTDB = "blast/aca_db"
GBK_PATH_BACT = "download_ncbi/bacteria_assembly_summary/"
GBK_PATH_ARCH = "download_ncbi/archaea_assembly_summary/"
GBK_PATH_VIRAL = "download_ncbi/viral_assembly_summary/"

GBK_PATHS = [GBK_PATH_BACT, GBK_PATH_ARCH, GBK_PATH_VIRAL]
#GBK_PATHS = [GBK_PATH_VIRAL]


BLASTOUTPUT = "blast"

def blast_anti_crispr_gendb():
    cmd = "{} -in {} -out {} -dbtype prot".format(MAKEBLASTDB_PATH, ACR_PROT_PATH, ACR_PROT_BLASTDB)
    os.system(cmd)

def blast_aca_gendb():
    cmd = "{} -in {} -out {} -dbtype prot".format(MAKEBLASTDB_PATH, ACA_PROT_PATH, ACA_PROT_BLASTDB)
    os.system(cmd)

def blast_anti_crispr_run():
    for to_remove in glob.glob("{}{}".format(BLAST_PATH, "*acrBlastpFiltered")):
        os.remove(to_remove)
    for domain in GBK_PATHS:
        for filename in os.listdir(domain):
            if filename.endswith(".faa.gz"):
                filename_out = filename.replace('.faa.gz', '.acrBlastpOut')
                filename_filtered = filename.replace('.faa.gz', '.acrBlastpFiltered')
                cmd = "zcat {}{} " \
                      "| {} -db {} -out {}{} -num_threads {} " \
                      "-outfmt \"6 qseqid sseqid qlen slen length pident gapopen evalue\" " \
                      "-evalue 0.01".format(
                    domain, filename,
                    BLASTP_PATH, ACR_PROT_BLASTDB,
                    BLAST_PATH, filename_out,
                    global_param.NUMBER_OF_THREADS)
                os.system(cmd)
                cmd = "awk -F '\t' '{{ if (($6>80) && ($3*0.8<$5)) {{print}} }}' {}{} > {}{}".format(
                    BLAST_PATH, filename_out,
                    BLAST_PATH, filename_filtered)
                os.system(cmd)
                os.remove("{}{}".format(BLAST_PATH, filename_out))

def blast_aca_run():
    for to_remove in glob.glob("{}{}".format(BLAST_PATH, "*acaBlastpFiltered")):
        os.remove(to_remove)
    for domain in GBK_PATHS:
        for filename in os.listdir(domain):
            if filename.endswith(".faa.gz"):
                filename_out = filename.replace('.faa.gz', '.acaBlastpOut')
                filename_filtered = filename.replace('.faa.gz', '.acaBlastpFiltered')
                cmd = "zcat {}{} " \
                      "| {} -db {} -out {}{} -num_threads {} " \
                      "-outfmt \"6 qseqid sseqid qlen slen length pident gapopen evalue\" " \
                      "-evalue 0.01".format(
                    domain, filename,
                    BLASTP_PATH, ACA_PROT_BLASTDB,
                    BLAST_PATH, filename_out,
                    global_param.NUMBER_OF_THREADS)
                os.system(cmd)
                cmd = "awk -F '\t' '{{ if (($6>80) && ($3*0.8<$5)) {{print}} }}' {}{} > {}{}".format(
                    BLAST_PATH, filename_out,
                    BLAST_PATH, filename_filtered)
                os.system(cmd)
                os.remove("{}{}".format(BLAST_PATH, filename_out))