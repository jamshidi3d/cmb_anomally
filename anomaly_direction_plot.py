import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

import cmb_anomaly_utils as cau
import read_maps_params as rmp

_inputs = rmp.get_inputs()

_inputs['geom_flag']    = cau.const.CAP_FLAG
_inputs['nsamples']     = _inputs['sampling_stop'] - _inputs['sampling_start'] + 1
sampling_range          = cau.stat_utils.get_sampling_range(**_inputs)


all_dir_anomaly = np.loadtxt("./output/direction_data.txt")

dir_nside = 16
'''nside for different pole directions'''
npix     = 12 * dir_nside ** 2
dir_lon, dir_lat = hp.pix2ang(dir_nside, np.arange(npix), lonlat = True)

def flatten_low_values_with_std(arr, nsigma = 1, flat_val = 0):
    copy_arr = np.copy(arr)
    top_val = np.max(arr) - nsigma * np.std(arr)
    _filter = arr < top_val
    copy_arr[_filter] = flat_val
    return copy_arr

def flatten_low_values_with_precent(arr, top_percent, flat_val = 0):
    copy_arr = np.copy(arr)
    top_val = np.max(arr) - top_percent / 100 * (np.max(arr) - np.min(arr))
    _filter = arr < top_val
    copy_arr[_filter] = flat_val
    return copy_arr

def colorize_special_pix(arr, index, factor = 0.25, from_min = True):
    copy_arr = np.copy(arr)
    diff = factor * (np.max(arr) - np.min(arr))
    copy_arr[index] = np.min(arr) - diff if from_min else np.max(arr) + diff
    return copy_arr


# stores the preference factor for selecting the anomaly direction
dir_pref = np.zeros(npix)
akrami_pix_index = hp.ang2pix(dir_nside, np.deg2rad(110), np.deg2rad(221))

for cap_size in range(10, 91, 1):
    fig, ax = plt.subplots()
    plt.axes(ax)
    cap_index = cau.stat_utils.get_nearest_index(sampling_range, cap_size)
    anom_arr = all_dir_anomaly[:, cap_index]
    dir_index = np.argmax(anom_arr)
    _title = r"$cap size = {}^\circ , lat|_{{max}} = {:0.1f}, lon|_{{max}} = {:0.1f}$".format(
        cap_size,
        dir_lat[dir_index],
        dir_lon[dir_index]
        )
    f_anom_arr = flatten_low_values_with_std(anom_arr, nsigma = 1, flat_val = 0)
    plot_f_anom_arr = colorize_special_pix(f_anom_arr, akrami_pix_index, factor = 0.4, from_min = True)
    hp.mollview(plot_f_anom_arr, title = _title, hold=True)
    fig.savefig(f"./output/dir_{cap_size}.jpg", transparent=True)
    plt.close(fig)
    dir_pref += f_anom_arr

dir_pref = flatten_low_values_with_std(dir_pref, nsigma = 1, flat_val = 0)
dir_pref = colorize_special_pix(dir_pref, akrami_pix_index, factor = 0.4, from_min = True)
fig, ax = plt.subplots()
plt.axes(ax)
_title = "Direction Preference Factor"
np.savetxt("./output/dir_preference.txt", dir_pref)
hp.mollview(dir_pref, title = _title, hold=True)
fig.savefig("./output/dir_preference.png", transparent=True)

