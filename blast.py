import os
import global_param

BLAST_PATH = "blast"
MAKEBLASTDB_PATH = "utils/blast/ncbi-blast-2.7.1+/bin/makeblastdb"
BLASTP_PATH = "utils/blast/ncbi-blast-2.7.1+/bin/blastp"
ACR_PROT_PATH = "download_acrdb/proteinSequence.faa"
ACR_PROT_BLASTDB = "blast/acrdb_db"
GBK_PATH_BACT = "download_ncbi/bacteria_assembly_summary/"
GBK_PATH_ARCH = "download_ncbi/archaea_assembly_summary/"
GBK_PATH_VIRAL = "download_ncbi/viral_assembly_summary/"
GBK_PATHS = [GBK_PATH_BACT, GBK_PATH_ARCH, GBK_PATH_VIRAL]


BLASTOUTPUT = "blast"

def blast_anti_crispr_gendb():
    cmd = "{} -in {} -out {} -dbtype prot".format(MAKEBLASTDB_PATH, ACR_PROT_PATH, ACR_PROT_BLASTDB)
    os.system(cmd)

def blast_anti_crispr_run():
    for domain in GBK_PATHS:
        for filename in os.listdir(domain):
            if filename.endswith(".faa.gz"):
                filename_out = filename.replace('.faa.gz', '.blastpOut')
                filename_filtered = filename.replace('.faa.gz', '.blastpFiltered')
                cmd = "zcat {}/{} " \
                      "| {} -db {} -out {}/{} -num_threads {} " \
                      "-outfmt \"6 qseqid sseqid qlen slen length pident gapopen evalue\" " \
                      "-evalue 0.001".format(
                    domain, filename,
                    BLASTP_PATH, ACR_PROT_BLASTDB,
                    BLAST_PATH, filename_out,
                    global_param.NUMBER_OF_THREADS)
                os.system(cmd)
                cmd = "awk -F $'\t' '{{ if (($6 > 90) && ($3>$5*0.9)) {{print}} }}' {}/{} > {}/{}".format(
                    BLAST_PATH, filename_out,
                    BLAST_PATH, filename_filtered)
                os.system(cmd)
