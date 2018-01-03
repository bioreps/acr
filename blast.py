import os
import glob
import global_param

BLAST_ACA_OUT = "blast/aca/blast_out/"
BLAST_ACR_OUT = "blast/acr/blast_out/"
MAKEBLASTDB_PATH = "utils/blast/ncbi-blast-2.7.1+/bin/makeblastdb"
BLASTP_PATH = "utils/blast/ncbi-blast-2.7.1+/bin/blastp"
ACR_PROT_PATH = "download_acrdb/proteinSequence_clust.faa" # here we use our own clustered db
ACA_PROT_PATH = "aca_seqs/acaSequences.faa"
ACR_PROT_BLASTDB = "blast/acr/db/"
ACA_PROT_BLASTDB = "blast/aca/db"
GBK_PATH_BACT = "download_ncbi/bacteria_assembly_summary/"
GBK_PATH_ARCH = "download_ncbi/archaea_assembly_summary/"
GBK_PATH_VIRAL = "download_ncbi/viral_assembly_summary/"

#GBK_PATHS = [GBK_PATH_BACT, GBK_PATH_ARCH, GBK_PATH_VIRAL]
GBK_PATHS = [GBK_PATH_BACT]


BLASTOUTPUT = "blast"

def blast_anti_crispr_gendb():
    cmd = "{} -in {} -out {} -dbtype prot".format(MAKEBLASTDB_PATH, ACR_PROT_PATH, ACR_PROT_BLASTDB)
    os.system(cmd)

def blast_aca_gendb():
    cmd = "{} -in {} -out {} -dbtype prot".format(MAKEBLASTDB_PATH, ACA_PROT_PATH, ACA_PROT_BLASTDB)
    os.system(cmd)

def blast_clean_folder():
    for to_remove in glob.glob("{}{}".format(BLAST_ACR_OUT, "*.blastpFiltered")):
        os.remove(to_remove)
    for to_remove in glob.glob("{}{}".format(BLAST_ACR_OUT, "*BlastpOut")):
        os.remove(to_remove)
    for to_remove in glob.glob("{}{}".format(BLAST_ACA_OUT, "*.blastpFiltered")):
        os.remove(to_remove)
    for to_remove in glob.glob("{}{}".format(BLAST_ACA_OUT, "*BlastpOut")):
        os.remove(to_remove)

def blast_anti_crispr_run(subset=999999):
    for domain in GBK_PATHS:
        subset_count = 0
        for filename in os.listdir(domain):
            if filename.endswith(".faa.gz"):
                filename_out = filename.replace('.faa.gz', '.acrBlastpOut')
                filename_filtered = filename.replace('.faa.gz', '.blastpFiltered')
                if os.path.exists(filename_filtered):
                    continue
                cmd = "zcat {}{} " \
                      "| {} -db {} -out {}{} -num_threads {} " \
                      "-outfmt \"6 qseqid sseqid qlen slen length pident gapopen evalue\" " \
                      "-evalue 0.01".format(
                    domain, filename,
                    BLASTP_PATH, ACR_PROT_BLASTDB,
                    BLAST_ACR_OUT, filename_out,
                    global_param.NUMBER_OF_THREADS)
                os.system(cmd)
                cmd = "awk -F '\t' '{{ if (($6>70) && ($3*0.7<$5)) {{print}} }}' {}{} >> {}{}".format(
                    BLAST_ACR_OUT, filename_out,
                    BLAST_ACR_OUT, filename_filtered)
                os.system(cmd)
                os.remove("{}{}".format(BLAST_ACR_OUT, filename_out))
            subset_count+=1
            if subset == subset_count:
                break

def blast_aca_run(subset=999999):
    for domain in GBK_PATHS:
        subset_count=0
        for filename in os.listdir(domain):
            if filename.endswith(".faa.gz"):
                filename_out = filename.replace('.faa.gz', '.acaBlastpOut')
                filename_filtered = filename.replace('.faa.gz', '.blastpFiltered')
                if os.path.exists(filename_filtered):
                    continue
                cmd = "zcat {}{} " \
                      "| {} -db {} -out {}{} -num_threads {} " \
                      "-outfmt \"6 qseqid sseqid qlen slen length pident gapopen evalue\" " \
                      "-evalue 0.01".format(
                    domain, filename,
                    BLASTP_PATH, ACA_PROT_BLASTDB,
                    BLAST_ACA_OUT, filename_out,
                    global_param.NUMBER_OF_THREADS)
                os.system(cmd)
                cmd = "awk -F '\t' '{{ if (($6>70) && ($3*0.7<$5)) {{print}} }}' {}{} >> {}{}".format(
                    BLAST_ACA_OUT, filename_out,
                    BLAST_ACA_OUT, filename_filtered)
                os.system(cmd)
                os.remove("{}{}".format(BLAST_ACA_OUT, filename_out))
            subset_count += 1
            if subset == subset_count:
                break