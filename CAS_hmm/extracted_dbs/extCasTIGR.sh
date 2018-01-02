#!/bin/bash

grep -B2 CRISPR ../raw_dbs/TIGRFAMs.hmm | grep ACC | sed 's/  */ /g' | cut -d$' ' -f2 > TIGRFAMs_namesCRISPR.txt
hmmfetch -f ../raw_dbs/TIGRFAMs.hmm TIGRFAMs_namesCRISPR.txt > TIGRFAMs_modelsCRISPR.hmm
