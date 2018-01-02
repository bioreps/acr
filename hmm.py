import os
import glob
import global_param

HMMSEARCH_PATH = "/usr/bin/hmmscan"
HMM_DBS = "hmm/cas/extracted_dbs/"
HMM_OUT = "hmm/cas/hmmscan_out/"
GBK_PATH_BACT = "download_ncbi/bacteria_assembly_summary/"
GBK_PATH_ARCH = "download_ncbi/archaea_assembly_summary/"
GBK_PATH_VIRAL = "download_ncbi/viral_assembly_summary/"

#GBK_PATHS = [GBK_PATH_BACT, GBK_PATH_ARCH, GBK_PATH_VIRAL]
GBK_PATHS = [GBK_PATH_BACT]

HMM_DB = [("tigr","TIGRFAMs_modelsCRISPR.hmm"),("pfam","Pfam-A_modelsCRISPR.hmm"),("novel","novel_modelsCRISPR.hmm")]

# WHAT: Clean folders of hmm runs.
def hmm_clean_folders():
    # Clean folder from Cas hits
    for to_remove in glob.glob("{}{}".format(HMM_OUT, "*.filtered")):
        os.remove(to_remove)
    for to_remove in glob.glob("{}{}".format(HMM_OUT, "*.out")):
        os.remove(to_remove)

# IDEA: Could we use jackhmmer here?

# WHAT: Runs hmmscan. Protein sequences of all genomes (individually) against all available hmm models of Cas proteins.
# IN: subset: defines how many protein sets to process (mainly for testing). Rest via files ("*.faa.gz").
# OUT: "*.hmmscan.cas.filtered"-files.
def hmm_run_cas(subset=999999):
    for domain in GBK_PATHS: # Iterate through all domains
        for (hmm_name, hmm_path) in HMM_DB: # Iterate through all hmm dbs
            subset_count = 0
            for filename in os.listdir(domain):
                if filename.endswith(".faa.gz"):
                    # Prepare filenames
                    filename_out = filename.replace('.faa.gz', '.'+hmm_name+'.out')
                    filename_filtered = filename.replace('.faa.gz', '.'+hmm_name+'.filtered')
                    if os.path.exists(filename_filtered):
                        continue
                    # Do a hmmscan run
                    cmd = "zcat {}{} " \
                          "| {} --cut_tc --cpu {} --tblout {}{} {}{} - >> /dev/null".format(
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
                    os.remove("{}{}".format(HMM_OUT, filename_out))
                subset_count += 1
                # If we did process enough genomes we stop.
                if subset == subset_count:
                    break