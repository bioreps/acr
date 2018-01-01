import download_ncbi
import download_acrdb
import blast

#download_ncbi.index_ncbi()
#download_ncbi.gbk_ncbi(onlyComplete=True, subset=999999)

#download_acrdb.acrdb()
#download_acrdb.acrdb_clust()


#blast.blast_anti_crispr_gendb()
#blast.blast_aca_gendb()

#blast.blast_clean_folder()

blast.blast_anti_crispr_run(subset=20)
blast.blast_aca_run(subset=20)