import sys
sys.path.insert(0, "..")
import xic
import pandas as pd
import download
import os

def test_resolve_remote_url():
    df = pd.read_csv("usi_list.tsv", sep='\t')
    for record in df.to_dict(orient="records"):
        remote_link = download._resolve_usi_remotelink(record["usi"])
        print(record["usi"], remote_link)

def test_resolve_download():
    df = pd.read_csv("usi_list.tsv", sep='\t')
    for record in df.to_dict(orient="records"):
        print(record["usi"])
        remote_link, local_filename = download._resolve_usi(record["usi"])

        assert(os.path.exists(local_filename))
        

def test_resolve_filename():
    df = pd.read_csv("usi_list.tsv", sep='\t')
    for record in df.to_dict(orient="records"):
        converted_filename = download._usi_to_local_filename(record["usi"])
        print(record["usi"], converted_filename)
    
def test_raw_filename():
    converted_filename = download._usi_to_local_filename("mzspec:PXD007600:20150416_41_F1_S28_ZT_1_4.raw")  # Should be in PRIDE
    converted_filename = download._usi_to_local_filename("mzspec:PXD022935:21720-TMT-Fra-1-1.raw")          # Should be in MassIVE

    # try:
    #     remote_link, local_filename = download._resolve_usi("mzspec:PXD022935:21720-TMT-Fra-1-1.raw")
    # except:
    #     raise
    #     pass

    # try:
    #     remote_link, local_filename = download._resolve_usi("mzspec:PXD007600:20150416_41_F1_S28_ZT_1_4.raw")
    # except:
    #     pass
    