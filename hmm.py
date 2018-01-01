import os
import glob
import global_param

HMM_PATH = "CAS_hmm/"
HMM_DBS = "CAS_hmm/extracted_dbs/"
HMM_OUT = "CAS_hmm/hmmsearch_out/"
GBK_PATH_BACT = "download_ncbi/bacteria_assembly_summary/"
GBK_PATH_ARCH = "download_ncbi/archaea_assembly_summary/"
GBK_PATH_VIRAL = "download_ncbi/viral_assembly_summary/"

#GBK_PATHS = [GBK_PATH_BACT, GBK_PATH_ARCH, GBK_PATH_VIRAL]
GBK_PATHS = [GBK_PATH_BACT]

HMM_DB = [("tigr","TIGRFAMs_modelsCRISPR.hmm"),("pfam","Pfam-A_modelsCRISPR.hmm"),("novel","novel_modelsCRISPR.hmm")]

def hmm_clean_folders():
    for to_remove in glob.glob("{}{}".format(HMM_OUT, "*.hmmsearchFiltered")):
        os.remove(to_remove)
    for to_remove in glob.glob("{}{}".format(HMM_OUT, "*.hmmsearchOut")):
        os.remove(to_remove)

def hmm_run(subset=999999):
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
                    BLAST_PATH, filename_out,
                    global_param.NUMBER_OF_THREADS)
                os.system(cmd)
                cmd = "awk -F '\t' '{{ if (($6>70) && ($3*0.7<$5)) {{print}} }}' {}{} >> {}{}".format(
                    BLAST_PATH, filename_out,
                    BLAST_PATH, filename_filtered)
                os.system(cmd)
                os.remove("{}{}".format(BLAST_PATH, filename_out))
            subset_count += 1
            if subset == subset_count:
                break