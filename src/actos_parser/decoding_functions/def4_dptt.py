import numpy as np
import re


def decode_dptt(raw_file):
    with open(raw_file, "r") as f:
        data = f.readlines()

    dptt = []
    for line in data:
        ptp, data = line.split("*")

        tt = int(data[:4], 16)
        ref = int(data[4:8], 16)
        dp = int(data[8:12], 16)

        u_dp = dp / 2**16 * 20 - 10
        u_tref = ref / 2**16 * 20 - 10
        u_tt = tt / 2**16 * 20 - 10

        t_ref = u_tref * 33.33 - 51.3
        u_r = t_ref * (38.346 + t_ref * (43.131 * 1e-3 - t_ref * 30.194 * 1e-6))

        x_dp = u_dp * 1e6 / 600 + u_r
        t_dp = x_dp * (26.056 * 1e-3 + x_dp * (-760.7 * 1e-9 + x_dp * 96.4 * 1e-12))

        x_tt = u_tt * 1e6 / 600 + u_r
        t_tt = x_tt * (26.056 * 1e-3 + x_tt * (-760.7 * 1e-9 + x_tt * 96.4 * 1e-12))

        dptt.append(f"{ptp},{t_dp},{t_ref},{t_tt}")
        # T_ref wird am Ende nicht mehr benötigt

    file_header = ["DATETIME,T_DP,T_REF,T_TT"]

    data = file_header + dptt

    return data
