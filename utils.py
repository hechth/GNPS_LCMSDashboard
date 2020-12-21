import pandas as pd
import requests
import uuid
import werkzeug
from scipy import integrate
import os
import sys
import pymzml
import json
import urllib.parse
from tqdm import tqdm
from time import sleep
from download import _resolve_usi

MS_precisions = {
    1 : 5e-6,
    2 : 20e-6,
    3 : 20e-6
}


import subprocess, io

def _calculate_file_stats(usi):
    remote_link, local_filename = _resolve_usi(usi)

    run = pymzml.run.Reader(local_filename, MS_precisions=MS_precisions)
    number_scans = run.get_spectrum_count()

    response_dict = {}
    response_dict["USI"] = usi
    response_dict["Scans"] = number_scans

    try:
        cmd = ["./bin/msaccess", local_filename, "-x",  'run_summary delimiter=tab']

        my_env = os.environ.copy()
        my_env["LC_ALL"] = "C"

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=my_env)
        out = proc.communicate()[0]

        all_lines = str(out).replace("\\t", "\t").split("\\n")
        all_lines = [line for line in all_lines if len(line) > 10 ]
        updated_version = "\n".join(all_lines)
        import sys
        print(updated_version, file=sys.stderr)
        data = io.StringIO(updated_version)
        df = pd.read_csv(data, sep="\t")
        
        record = df.to_dict(orient='records')[0]

        fields = ["Vendor", "Model", "MS1s", "MS2s"]
        for field in fields:
            if field in record:
                response_dict[field] = record[field]
            else:
                response_dict[field] = "N/A"
    except:
        pass
    
    return response_dict

# Gets Positive and Negative return values, or None
def _get_scan_polarity(spec):
    # Determining scan polarity
    polarity = None
    try:
        if spec["negative scan"] is True:
            polarity = "Negative"
        if spec["positive scan"] is True:
            polarity = "Positive"
    except:    
        pass
     
    return polarity

# Given URL, will try to parse and get key
def _get_param_from_url(search, url_hash, param_key, default):

    try:
        params_dict = urllib.parse.parse_qs(search[1:])
        if param_key in params_dict:
            return str(params_dict[param_key][0])
    except:
        pass

    try:
        hash_dict = json.loads(urllib.parse.unquote(url_hash[1:]))
        if param_key in hash_dict:
            return str(hash_dict[param_key])
    except:
        pass

    return default

def _resolve_map_plot_selection(url_search, usi):
    current_map_selection = {}
    highlight_box = None

    # Lets start off with taking the url bounds
    try:
        current_map_selection = json.loads(_get_param_from_url(url_search, "", "map_plot_zoom", "{}"))
    except:
        pass

    try:
        usi_splits = usi.split(":")
        dataset = usi_splits[1]
        filename = usi_splits[2]

        if len(usi_splits) > 3 and usi_splits[3] == "scan":
            scan_number = int(usi_splits[4])

            if scan_number == 1:
                # Lets get out of here and not set anything
                raise Exception
            
            remote_link, local_filename = _resolve_usi(usi)
            run = pymzml.run.Reader(local_filename, MS_precisions=MS_precisions)
            spec = run[scan_number]
            rt = spec.scan_time_in_minutes()
            mz = spec.selected_precursors[0]["mz"]

            min_rt = max(rt - 0.5, 0)
            max_rt = rt + 0.5

            min_mz = mz - 3
            max_mz = mz + 3

            # If this is already set in the URL, we don't overwrite
            if len(current_map_selection) == 0 or "autosize" in current_map_selection:
                current_map_selection["xaxis.range[0]"] = min_rt
                current_map_selection["xaxis.range[1]"] = max_rt
                current_map_selection["yaxis.range[0]"] = min_mz
                current_map_selection["yaxis.range[1]"] = max_mz

            highlight_box = {}
            highlight_box["left"] = rt - 0.01
            highlight_box["right"] = rt + 0.01
            highlight_box["top"] = mz + 0.1
            highlight_box["bottom"] = mz - 0.1
    except:
        pass

    return current_map_selection, highlight_box


def _determine_rendering_bounds(map_selection):
    min_rt = 0
    max_rt = 1000000
    min_mz = 0
    max_mz = 2000

    if map_selection is not None:
        if "xaxis.range[0]" in map_selection:
            min_rt = float(map_selection["xaxis.range[0]"])
        if "xaxis.range[1]" in map_selection:
            max_rt = float(map_selection["xaxis.range[1]"])

        if "yaxis.range[0]" in map_selection:
            min_mz = float(map_selection["yaxis.range[0]"])
        if "yaxis.range[1]" in map_selection:
            max_mz = float(map_selection["yaxis.range[1]"])

    return min_rt, max_rt, min_mz, max_mz

# Binary Search, returns target
def _find_lcms_rt(filename, rt_query):
    run = pymzml.run.Reader(filename, MS_precisions=MS_precisions)

    s = 0
    e = run.get_spectrum_count()

    while True:
        jump_point = int((e + s) / 2)
        print("BINARY SEARCH", jump_point)

        # Jump out early
        if jump_point == 0:
            break
        
        if jump_point == run.get_spectrum_count():
            break

        if s == e:
            break

        if e - s == 1:
            break

        spec = run[ jump_point ]

        if spec.scan_time_in_minutes() < rt_query:
            s = jump_point
        elif spec.scan_time_in_minutes() > rt_query:
            e = jump_point
        else:
            break

    return e


def _spectrum_generator(filename, min_rt, max_rt):
    run = pymzml.run.Reader(filename, MS_precisions=MS_precisions)

    # Don't do this if the min_rt and max_rt are not reasonable values
    if min_rt <= 0 and max_rt > 1000:
        for spec in run:
            yield spec

    else:
        try:
            min_rt_index = _find_lcms_rt(filename, min_rt) # These are inclusive on left
            max_rt_index = _find_lcms_rt(filename, max_rt) + 1 # Exclusive on the right

            for spec_index in tqdm(range(min_rt_index, max_rt_index)):
                spec = run[spec_index]
                yield spec
            print("USED INDEX")
        except:
            for spec in run:
                yield spec
            print("USED BRUTEFORCE")

# Getting the Overlay data
def _resolve_overlay(overlay_usi, overlay_mz, overlay_rt, overlay_filter_column, overlay_filter_value, overlay_size, overlay_color, overlay_hover):
    overlay_usi_splits = overlay_usi.split(":")
    file_path = overlay_usi_splits[2].split("-")[-1]
    task = overlay_usi_splits[2].split("-")[1]
    url = "http://massive.ucsd.edu/ProteoSAFe/DownloadResultFile?task={}&block=main&file={}".format(task, file_path)
    overlay_df = pd.read_csv(url, sep=None, nrows=20000)

    overlay_df["mz"] = overlay_df[overlay_mz]
    overlay_df["rt"] = overlay_df[overlay_rt]

    # Filtering
    if len(overlay_filter_column) > 0 and overlay_filter_column in overlay_df:
        if len(overlay_filter_value) > 0:
            overlay_df = overlay_df[overlay_df[overlay_filter_column] == overlay_filter_value]

    # Adding Size
    if len(overlay_size) > 0 and overlay_size in overlay_df:
        overlay_df["size"] = overlay_df[overlay_size]
    
    # Adding Color
    if len(overlay_color) > 0 and overlay_color in overlay_df:
        overlay_df["color"] = overlay_df[overlay_color]
    
    
    # Adding Label
    if len(overlay_hover) > 0 and overlay_hover in overlay_df:
        overlay_df["hover"] = overlay_df[overlay_hover]

    return overlay_df