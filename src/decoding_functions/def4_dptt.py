import re


def decode_dptt(raw_file):
    with open(raw_file, "r") as f:
        data = f.readlines()

    dptt = []
    for line in data:
        ptp = line.split("*")[0]

        u_1 = int(line.split("*")[1][:4], 16)
        u_2 = int(line.split("*")[1][4:8], 16)
        u_3 = int(line.split("*")[1][8:12], 16)

        dptt.append(f"{ptp},{u_1},{u_2},{u_3}")

    file_header = ["DATETIME,U_1,U_2,U_3"]

    data = file_header + dptt

    return data
