import re


def decode_pvm(raw_file):
    with open(raw_file, "r") as f:
        data = f.readlines()

    pvm = []
    for line in data:
        ptp = line.split("*")[0]

        lwc1 = int(line.split("*")[1][:4], 16)
        lwc2 = int(line.split("*")[1][4:8], 16)
        psa1 = int(line.split("*")[1][8:12], 16)
        psa2 = int(line.split("*")[1][12:], 16)

        lwc1 = lwc1 / 2**16 * 5
        lwc2 = lwc2 / 2**16 * 5
        psa1 = psa1 / 2**16 * 5
        psa2 = psa2 / 2**16 * 5

        pvm.append(f"{ptp},{lwc1},{lwc2},{psa1},{psa2}")

    file_header = ["DATETIME,LWC_1,LWC_2,PSA_1,PSA_2"]

    data = file_header + pvm

    return data
