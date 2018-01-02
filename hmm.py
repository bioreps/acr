import os
import glob
import global_param

HMMSEARCH_PATH = "/usr/bin/hmmscan"
HMM_PATH = "CAS_hmm/"
HMM_DBS = "CAS_hmm/extracted_dbs/"
HMM_OUT = "CAS_hmm/hmmscan_out/"
GBK_PATH_BACT = "download_ncbi/bacteria_assembly_summary/"
GBK_PATH_ARCH = "download_ncbi/archaea_assembly_summary/"
GBK_PATH_VIRAL = "download_ncbi/viral_assembly_summary/"

#GBK_PATHS = [GBK_PATH_BACT, GBK_PATH_ARCH, GBK_PATH_VIRAL]
GBK_PATHS = [GBK_PATH_BACT]

HMM_DB = [("tigr","TIGRFAMs_modelsCRISPR.hmm"),("pfam","Pfam-A_modelsCRISPR.hmm"),("novel","novel_modelsCRISPR.hmm")]

def hmm_clean_folders():
    # Clean folder from Cas hits
    for to_remove in glob.glob("{}{}".format(HMM_OUT, "*.hmmscan.cas.filtered")):
        os.remove(to_remove)
    for to_remove in glob.glob("{}{}".format(HMM_OUT, "*.hmmscan.cas.out")):
        os.remove(to_remove)

# IDEA: Could we use jackhmmer here?

# WHAT: Runs hmmscan. Protein sequences of all genomes (individually) against all available hmm models of Cas proteins
def hmm_run(subset=999999):
    for domain in GBK_PATHS:
        for (hmm_name, hmm_path) in HMM_DB:
            subset_count = 0
            for filename in os.listdir(domain):
                if filename.endswith(".faa.gz"):
                    filename_out = filename.replace('.faa.gz', '.'+hmm_name+'.hmmscan.cas.out')
                    filename_filtered = filename.replace('.faa.gz', '.'+hmm_name+'.hmmscan.cas.filtered')
                    if os.path.exists(filename_filtered):
                        continue
                    # Do a hmmscan run
                    cmd = "zcat {}{} " \
                          "| {} -E 1e-15 --domE 1e-15 --cpu {} --tblout {}{} {}{} - >> CAS_hmm/hmmscan_out/text.txt".format(
                        domain, filename,
                        HMMSEARCH_PATH, global_param.NUMBER_OF_THREADS,
                        HMM_OUT, filename_out,
                        HMM_DBS, hmm_path
                    )
                    os.system(cmd)
                    # kick out the comment lines and just keep the best hit
                    cmd = "sed 's/  */ /g' {}{} | grep -v ^# | awk '!seen[$3]++' >> {}{}".format(
                        HMM_OUT, filename_out,
                        HMM_OUT, filename_filtered)
                    os.system(cmd)
                    #os.remove("{}{}".format(HMM_OUT, filename_out))
                subset_count += 1
                if subset == subset_count:
                    break