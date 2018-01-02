#!/bin/bash

grep -B2 CRISPR ../raw_dbs/Pfam-A.hmm | grep ACC | sed 's/  */ /g' | cut -d$' ' -f2 > Pfam-A_namesCRISPR.txt
hmmfetch -f ../raw_dbs/Pfam-A.hmm Pfam-A_namesCRISPR.txt > Pfam-A_modelsCRISPR.hmm
