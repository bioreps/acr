import urllib3

INDEX_URL = "https://ftp.ncbi.nlm.nih.gov/genomes/refseq/archaea/assembly_summary.txt"
INDEX_PATH = "download/assembly_summary.txt"

http = urllib3.PoolManager()
r = http.request('GET', INDEX_URL, preload_content=False)

with open(INDEX_PATH, 'wb') as out:
    while True:
        data = r.read()
        if not data:
            break
        out.write(data)

r.release_conn()