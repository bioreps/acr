import os
import glob
from global_param import *

class hmm_clean(object):
    def __init__(self, target_folder, filetypes):
        self.target_folder = target_folder
        self.filetypes = filetypes
    def clean_folder(self):
        for ft in self.filetypes:
            for to_remove in glob.glob("{}{}".format(self.target_folder, ft)):
                os.remove(to_remove)


# IDEA: Could we use jackhmmer here?

# WHAT: Runs hmmscan. Protein sequences of all genomes (individually) against all available hmm models of Cas proteins.
# IN: subset: defines how many protein sets to process (mainly for testing). Rest via files ("*.faa.gz").
# OUT: "*.hmmscan.cas.filtered"-files.
def hmm_run_cas(domains, subset=999999):
    for domain in domains: # Iterate through all domains
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
                          "| {} -E 1e-7 --cpu {} --tblout {}{} {}{} - >> /dev/null".format( #"| {} --cut_tc --cpu {} --tblout {}{} {}{} - >> /dev/null".format(
                        domain, filename,
                        HMMSEARCH_PATH, NUMBER_OF_THREADS,
                        HMM_CAS_OUT, filename_out,
                        HMM_CAS_DBS, hmm_path
                    )
                    os.system(cmd)
                    # kick out the comment lines and just keep the best hit
                    cmd = "sed 's/  */ /g' {}{} | grep -v ^# | awk '!seen[$3]++' >> {}{}".format(
                        HMM_CAS_OUT, filename_out,
                        HMM_CAS_OUT, filename_filtered)
                    os.system(cmd)
                    os.remove("{}{}".format(HMM_CAS_OUT, filename_out))
                subset_count += 1
                # If we did process enough genomes we stop.
                if subset == subset_count:
                    break