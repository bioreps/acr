NUMBER_OF_THREADS = 4

GBK_PATH_BACT = "download_ncbi/bacteria_assembly_summary/"
GBK_PATH_ARCH = "download_ncbi/archaea_assembly_summary/"
GBK_PATH_VIRAL = "download_ncbi/viral_assembly_summary/"

BLAST_ACA_OUT = "blast/aca/blast_out/"
BLAST_ACR_OUT = "blast/acr/blast_out/"
MAKEBLASTDB_PATH = "utils/blast/ncbi-blast-2.7.1+/bin/makeblastdb"
BLASTP_PATH = "utils/blast/ncbi-blast-2.7.1+/bin/blastp"
ACR_PROT_PATH = "download_acrdb/proteinSequence_clust.faa" # here we use our own clustered db
ACA_PROT_PATH = "aca_seqs/acaSequences.faa"
ACR_PROT_BLASTDB = "blast/acr/db/acr"
ACA_PROT_BLASTDB = "blast/aca/db/aca"

HMMSEARCH_PATH = "/usr/bin/hmmscan"
HMM_CAS_DBS = "hmm/cas/extracted_dbs/"
HMM_CAS_OUT = "hmm/cas/hmmscan_out/"
HMM_DB = [("tigr","TIGRFAMs_modelsCRISPR.hmm"),("pfam","Pfam-A_modelsCRISPR.hmm"),("novel","novel_modelsCRISPR.hmm")]

PILERCR_PATH = "/home/michael/Software/pilercr/pilercr1.06/pilercr"