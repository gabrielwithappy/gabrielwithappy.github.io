#!/bin/bash
source .venv/bin/activate
echo "Starts update data files"

python3 generate_datafile.py -graph_name kospi_mdd -key $1
echo ">> updated KOSPI MDD Graph"
python3 generate_datafile.py -graph_name sp500_mdd -key $1
echo ">> updated SP500 MDD Graph"
python3 generate_datafile.py -graph_name kospi_monthly_returns -key $1
echo ">> updated KOSPI Monthly Returns"
python3 generate_datafile.py -graph_name sp500_monthly_returns -key $1
echo ">> updated SP500 Monthly Returns"
python3 generate_datafile.py -graph_name korea_nsi -key $1
echo ">> updated KOSPI NSI Returns"
echo ">> Finish update data files >>"

