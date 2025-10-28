from datetime import datetime, timedelta
import re


def decode_pvm(raw_file):
    with open(raw_file, "r") as f:
        data = f.readlines()

    pvm = []
    for line in data:
        ptp1, data = line.split("*")
        try:
            ptp_temp = datetime.strptime(ptp1, "%Y-%m-%d %H:%M:%S.%f")
        except:
            ptp_temp = datetime.strptime(ptp1, "%Y-%m-%d %H:%M:%S")
        ptp2 = ptp_temp + timedelta(milliseconds=1)
        try:
            ptp2 = datetime.strftime(ptp2, "%Y-%m-%d %H:%M:%S.%f")
        except:
            ptp2 = datetime.strftime(ptp2, "%Y-%m-%d %H:%M:%S")

        lwc1 = int(data[:4], 16)
        lwc2 = int(data[4:8], 16)
        psa1 = int(data[8:12], 16)
        psa2 = int(data[12:], 16)

        u_lwc1 = lwc1 / 2**16 * 5
        u_lwc2 = lwc2 / 2**16 * 5
        lwc1 = u_lwc1
        lwc2 = u_lwc2

        u_psa1 = psa1 / 2**16 * 5
        u_psa2 = psa2 / 2**16 * 5
        psa1 = u_psa1 * 2980
        psa2 = u_psa2 * 2980

        if not u_psa1 == 0:
            r_eff1 = (u_lwc1 / u_psa1) * 10
        else:
            r_eff1 = -999
        if not u_psa2 == 0:
            r_eff2 = (u_lwc2 / u_psa2) * 10
        else:
            r_eff2 = -999

        pvm.append(f"{ptp1},{lwc1},{psa1},{r_eff1}")
        pvm.append(f"{ptp2},{lwc2},{psa2},{r_eff2}")

    file_header = ["DATETIME,LWC,PSA,R_EFF"]

    data = file_header + pvm

    return data
