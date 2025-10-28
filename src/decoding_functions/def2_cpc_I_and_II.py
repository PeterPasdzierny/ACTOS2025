import re


def decode_cpc_I_and_II(raw_file):
    with open(raw_file, "r") as f:
        data = f.readlines()

    cpcs = []
    for line in data:
        ptp, data = line.split("*")

        cpc1 = int(data[:4], 16)
        cpc2 = int(data[4:], 16)

        cpc1 = cpc1 * 10 * 2 * 60 / 1500
        cpc2 = cpc2 * 10 * 2 * 60 / 1500

        cpcs.append(f"{ptp},{cpc1},{cpc2}")

    file_header = ["DATETIME,CPCI,CPCII"]

    data = file_header + cpcs

    return data
