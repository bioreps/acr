import download_ncbi
import download_acrdb
import blast
import hmm
from global_param import *

#GBK_PATHS = [GBK_PATH_BACT, GBK_PATH_ARCH, GBK_PATH_VIRAL]
GBK_PATHS = [GBK_PATH_BACT]

#download_ncbi.index_ncbi()
#download_ncbi.gbk_ncbi(onlyComplete=True, subset=999999)

#download_acrdb.acrdb()
#download_acrdb.acrdb_clust()

#blast.blast_anti_crispr_gendb()
#blast.blast_aca_gendb()

clean_acr = blast.blast_clean(BLAST_ACR_OUT, ["*.filtered", "*.out"])
clean_acr.clean_folder()
clean_aca = blast.blast_clean(BLAST_ACA_OUT, ["*.filtered", "*.out"])
clean_aca.clean_folder()

blast.blast_anti_crispr_run(GBK_PATHS, subset=20)
blast.blast_aca_run(GBK_PATHS,subset=20)

# clean_cas = hmm.hmm_clean(HMM_CAS_OUT, ["*.filtered", "*.out"])
# clean_cas.clean_folder()

# hmm.hmm_run_cas(GBK_PATHS, subset=200)