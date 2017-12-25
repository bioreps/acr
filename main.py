import download_ncbi
import download_acrdb
import blast

download_ncbi.index_ncbi()
download_ncbi.gbk_ncbi(onlyComplete=True, subset=999999)

download_acrdb.acrdb()

blast.blast_anti_crispr_gendb()
blast.blast_anti_crispr_run()