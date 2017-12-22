import urllib3
import certifi

URL_PROT = "http://cefg.uestc.edu.cn/anti-CRISPRdb/dataset/proteinSequence.faa"
NAME_PROT = "proteinSequence.faa"
URL_PROT_NR = "http://cefg.uestc.edu.cn/anti-CRISPRdb/dataset/non-redundant.zip"
NAME_PROT_NR = "non-redundant.zip"
URL_NUC = "http://cefg.uestc.edu.cn/anti-CRISPRdb/dataset/nucleotideSequences.fna"
NAME_NUC = "nucleotideSequences.fna"
# similarity data not downloaded so far

TARGET_PATH = "download_acrdb"

FILES_TO_FETCH = [(URL_PROT, NAME_PROT), (URL_PROT_NR, NAME_PROT_NR), (URL_NUC, NAME_NUC)]

http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())


def acrdb():
    for (url, filename) in FILES_TO_FETCH:
        r = http.request('GET', url, preload_content=False)
        with open('{}/{}'.format(TARGET_PATH, filename), 'wb') as out:
            while True:
                data = r.read()
                if not data:
                    break
                out.write(data)
        r.release_conn()
