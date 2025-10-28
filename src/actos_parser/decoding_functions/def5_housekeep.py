import re


def decode_housekeep(raw_file):
    with open(raw_file, "r") as f:
        data = f.readlines()

    housekeep = []
    for line in data:
        ptp, data = line.split("*")

        cws_switch = int(data[:4], 16)
        filter_switch = int(data[4:8], 16)
        th_1 = int(data[8:12], 16)
        th_2 = int(data[12:16], 16)
        u_12 = int(data[16:20], 16)
        u_24 = int(data[20:24], 16)
        u_28 = int(data[24:28], 16)
        um_15 = int(data[28:32], 16)
        up_15 = int(data[32:36], 16)

        cws_switch = cws_switch / 2**16 * 20 - 10
        filter_switch = filter_switch / 2**16 * 20 - 10
        th_1 = (th_1 / 2**16 * 20 - 10) * 115 - 25
        th_2 = (th_2 / 2**16 * 20 - 10) * 115 - 25
        u_12 = (u_12 / 2**16 * 20 - 10) * 3
        u_24 = (u_24 / 2**16 * 20 - 10) * 3
        u_28 = (u_28 / 2**16 * 20 - 10) * 3
        um_15 = (um_15 / 2**16 * 20 - 10) * 3
        up_15 = (up_15 / 2**16 * 20 - 10) * 3

        housekeep.append(
            f"{ptp},{cws_switch},{filter_switch},{th_1},{th_2},{u_12},{u_24},{u_28},{um_15},{up_15}"
        )

    file_header = [
        "DATETIME,CWS_SWITCH,FILTER_SWITCH,TH_1,TH_2,U_12,U_24,U_28,UM_15,UP_15"
    ]

    data = file_header + housekeep

    return data
