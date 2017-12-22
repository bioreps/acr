import urllib3
import urllib
import certifi
import shutil
import os
import csv

INDEX_URL_BACT = "https://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/assembly_summary.txt"
INDEX_PATH_BACT = "download/bacteria_assembly_summary.txt"
GBK_PATH_BACT = "download/bacteria_assembly_summary/"
INDEX_URL_ARCH = "https://ftp.ncbi.nlm.nih.gov/genomes/refseq/archaea/assembly_summary.txt"
INDEX_PATH_ARCH = "download/archaea_assembly_summary.txt"
GBK_PATH_ARCH = "download/archaea_assembly_summary/"
INDEX_URL_VIRAL = "https://ftp.ncbi.nlm.nih.gov/genomes/refseq/viral/assembly_summary.txt"
INDEX_PATH_VIRAL = "download/viral_assembly_summary.txt"
GBK_PATH_VIRAL = "download/viral_assembly_summary/"

INDEX = [(INDEX_URL_BACT, INDEX_PATH_BACT), (INDEX_URL_ARCH, INDEX_PATH_ARCH), (INDEX_URL_VIRAL, INDEX_PATH_VIRAL)]
STORES = [(INDEX_PATH_BACT, GBK_PATH_BACT), (INDEX_PATH_ARCH, GBK_PATH_ARCH), (INDEX_PATH_VIRAL, GBK_PATH_VIRAL)]

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


def gbk_ncbi():
    for (index_path, path_store) in STORES:

        if os.path.exists(os.path.abspath(path_store)):
            shutil.rmtree(os.path.abspath(path_store))
        os.makedirs(os.path.abspath(path_store))

        with open(index_path) as f:
            reader = csv.reader(f, delimiter='\t')

            first_header_line = next(reader)
            second_header_line = next(reader)

            for row in reader:
                gbk_url = '{}/{}_{}_genomic.gbff.gz'.format(row[19].replace('ftp://','https://'), row[0], row[15])
                filename_url = '{}_{}_genomic.gbff.gz'.format(row[0], row[15])
                print(gbk_url)

                r = http.request('GET', gbk_url, preload_content=False)
                with open(os.path.abspath(path_store+filename_url), 'wb') as out:
                    while True:
                        data = r.read()
                        if not data:
                            break
                        out.write(data)
                r.release_conn()
