import urllib3
import certifi
import shutil
import os
import csv

COLUMN_NAMES = ["assembly_accession", "bioproject", "biosample", "wgs_master",
                "refseq_category", "taxid", "species_taxid", "organism_name",
                "infraspecific_name", "isolate", "version_status", "assembly_level",
                "release_type", "genome_rep", "seq_rel_date", "asm_name", "submitter",
                "gbrs_paired_asm", "paired_asm_comp", "ftp_path", "excluded_from_refseq",
                "relation_to_type_material",
                ]

INDEX_URL_BACT = "https://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/assembly_summary.txt"
INDEX_PATH_BACT = "download_ncbi/bacteria_assembly_summary.txt"
GBK_PATH_BACT = "download_ncbi/bacteria_assembly_summary/"
INDEX_URL_ARCH = "https://ftp.ncbi.nlm.nih.gov/genomes/refseq/archaea/assembly_summary.txt"
INDEX_PATH_ARCH = "download_ncbi/archaea_assembly_summary.txt"
GBK_PATH_ARCH = "download_ncbi/archaea_assembly_summary/"
INDEX_URL_VIRAL = "https://ftp.ncbi.nlm.nih.gov/genomes/refseq/viral/assembly_summary.txt"
INDEX_PATH_VIRAL = "download_ncbi/viral_assembly_summary.txt"
GBK_PATH_VIRAL = "download_ncbi/viral_assembly_summary/"

INDEX = [(INDEX_URL_BACT, INDEX_PATH_BACT), (INDEX_URL_ARCH, INDEX_PATH_ARCH), (INDEX_URL_VIRAL, INDEX_PATH_VIRAL)]
STORES = [(INDEX_PATH_BACT, GBK_PATH_BACT), (INDEX_PATH_ARCH, GBK_PATH_ARCH), (INDEX_PATH_VIRAL, GBK_PATH_VIRAL)]

TYPES = ["genomic.gbff.gz", "protein.faa.gz", "genomic.fna.gz"]

http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())


def index_ncbi():
    for (index_url, index_path) in INDEX:
        r = http.request('GET', index_url, preload_content=False)
        with open(index_path, 'wb') as out:
            while True:
                data = r.read()
                if not data:
                    break
                out.write(data)
        r.release_conn()


def gbk_ncbi(onlyComplete = False):
    for (index_path, path_store) in STORES:

        if os.path.exists(os.path.abspath(path_store)):
            shutil.rmtree(os.path.abspath(path_store))
        os.makedirs(os.path.abspath(path_store))

        with open(index_path) as f:
            reader = csv.reader(f, delimiter='\t', names=COLUMN_NAMES)

            first_header_line = next(reader)
            second_header_line = next(reader)e

            for row in reader:

                if onlyComplete == True and row[11] != "complete":
                    continue

                for type in TYPES:
                    gbk_url = '{}/{}_{}_{}'.format(row[19].replace('ftp://','https://'), row[0], row[15], type)
                    filename_url = '{}_{}_{}'.format(row[0], row[15], type)
                    print(gbk_url)

                    r = http.request('GET', gbk_url, preload_content=False)
                    with open(os.path.abspath(path_store+filename_url), 'wb') as out:
                        while True:
                            data = r.read()
                            if not data:
                                break
                            out.write(data)
                    r.release_conn()
