import urllib3
import certifi

INDEX_URL_BACT = "https://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/assembly_summary.txt"
INDEX_PATH_BACT = "download/bacteria_assembly_summary.txt"
INDEX_URL_ARCH = "https://ftp.ncbi.nlm.nih.gov/genomes/refseq/archaea/assembly_summary.txt"
INDEX_PATH_ARCH = "download/archarea_assembly_summary.txt"
INDEX_URL_VIRAL = "https://ftp.ncbi.nlm.nih.gov/genomes/refseq/viral/assembly_summary.txt"
INDEX_PATH_VIRAL = "download/viral_assembly_summary.txt"

INDEX = [(INDEX_URL_BACT,INDEX_PATH_BACT),(INDEX_URL_ARCH,INDEX_PATH_ARCH),(INDEX_URL_VIRAL,INDEX_PATH_VIRAL)]

http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())

for (index_url,index_path) in INDEX:
    r = http.request('GET', index_url, preload_content=False)
    with open(index_path, 'wb') as out:
        while True:
            data = r.read()
            if not data:
                break
            out.write(data)

r.release_conn()