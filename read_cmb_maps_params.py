#
#
# This script provides a faster way to read maps and inputs!
#
#

import json
import cmb_anomaly_utils as cau

cmb_fpath               = "./input/cmb_fits_files/COM_CMB_IQU-commander_2048_R3.00_full.fits"
mask_fpath              = "./input/cmb_fits_files/COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits"
input_params_fpath      = './input/run_parameters.json'

def get_inputs():
    json_inputs_file =  open(input_params_fpath,'r')
    _inputs = json.loads(json_inputs_file.read())
    json_inputs_file.close()
    return _inputs

def print_inputs(input_dict):
    max_key_len = 20
    for key, val in zip(input_dict.keys(), input_dict.values()):
        if "comment" in key.lower():
            continue
        print("-" + " " * (max_key_len - len(key)) + key, ":", val)
    for i in range(2) : print("*" * 40)

def get_cmb_pixdata(**inputs):
    sky_pix = cau.map_reader.get_data_pix_from_cmb(cmb_fpath, mask_fpath, **inputs)
    return sky_pix