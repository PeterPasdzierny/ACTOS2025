import re


def decode_ptb(raw_file):
    with open(raw_file, "r") as f:
        data = f.readlines()

    data = [
        (
            line.split("*")[0],
            bytes.fromhex(line.split("*")[1]).replace(b"\x00", b"").decode("ascii"),
        )
        for line in data
    ]

    sli = [i for i, line in enumerate(data) if "PTB" in line[1]]

    ptb = []
    for i in sli[:-1]:
        if "P" in data[i + 1]:
            ptb.append(
                # data[i][0] + "," + re.sub(r"[PTB\s+]", "", data[i][1])
                data[i][0] + "," + "-999"
            )  # oder besser NaN/-999 einfügen, statt des ggfls. unvollständigen wertes?
        if not "PTB" in data[i + 1]:
            # else:
            ptb.append(
                data[i][0]
                + ","
                + re.sub(r"[PTB\s+]", "", data[i][1])
                + re.sub(r"[PTB\s+]", "", data[i + 1][1])
            )

    file_header = ["DATETIME,PRESSURE_PTB"]

    data = file_header + ptb

    return data
