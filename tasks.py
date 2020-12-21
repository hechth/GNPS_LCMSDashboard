from celery import Celery
import download
import os
import uuid
import feature_finding
import xic
from joblib import Memory
memory = Memory("/app/temp/xic-cache", verbose=0)

# Setting up celery
celery_instance = Celery('lcms_tasks', backend='redis://redis', broker='redis://redis')

##############################
# Conversion
##############################
@celery_instance.task(time_limit=240)
def _download_convert_file(usi, temp_folder="temp"):
    """
        This function does the serialization of downloading files
    """

    return download._resolve_usi(usi, temp_folder=temp_folder)

#################################
# Compute Data
#################################
@celery_instance.task(time_limit=60)
def task_xic(local_filename, all_xic_values, xic_tolerance, xic_ppm_tolerance, xic_tolerance_unit, rt_min, rt_max, polarity_filter, get_ms2=False):
    # Caching
    xic_file = memory.cache(xic.xic_file)

    xic_df, ms2_data = xic_file(local_filename, all_xic_values, xic_tolerance, xic_ppm_tolerance, xic_tolerance_unit, rt_min, rt_max, polarity_filter, get_ms2=get_ms2)
    return xic_df.to_dict(orient="records"), ms2_data

@celery_instance.task(time_limit=60)
def task_featurefinding(filename, params):
    feature_df = feature_finding.perform_feature_finding(filename, params)
    return feature_df.to_dict(orient="records")


@celery_instance.task(time_limit=60)
def task_computeheartbeat():
    return "Up"


celery_instance.conf.task_routes = {
    'tasks._download_convert_file': {'queue': 'conversion'},
    'tasks.task_xic': {'queue': 'compute'},
    'tasks.task_featurefinding': {'queue': 'compute'},
    'tasks.task_computeheartbeat': {'queue': 'compute'},
}