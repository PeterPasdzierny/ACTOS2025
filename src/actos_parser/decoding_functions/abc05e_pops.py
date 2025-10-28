import re


def decode_pops(raw_file):
    with open(raw_file, "r") as f:
        data = f.readlines()

    data = [
        (
            line.split("*")[0],
            bytes.fromhex(line.split("*")[1][20:])
            .replace(b"\x00", b"")
            .replace(b"\x0d", b"")
            .decode("ascii"),
        )
        for line in data
    ]

    sli = [i for i, line in enumerate(data) if "POPS" in line[1]]
    offset = sli[0]
    eli = [i for i, line in enumerate(data[sli[0] :]) if "\n" in line[1]]
    if len(sli) > len(eli):
        sli = sli[: len(eli)]
    sei = [(sli[i], eli[i]) for i in range(len(sli))]

    pops = []
    for s in sei:
        current = []
        current.append(data[s[0]][0])
        current.append(",")

        for i in range(s[0], s[1] + offset + 1):
            line = data[i][1]
            current.append(line)
        current = "".join(current)

        current = re.sub(r"POPS\,", "", current)
        current = re.sub(r"nan", "-999", current)
        # current = re.sub(r"\d{8}T\d{6},", "", current)
        current = current.rstrip("\n")
        pops.append(current)

    file_header = [
        "DATETIME,DATETIME_POPS,1_POPS,2_POPS,3_POPS,4_POPS,5_POPS,6_POPS,7_POPS,8_POPS,9_POPS,10_POPs,11_POPS,12_POPS,13_POPS,14_POPs,15_POPS,16_POPS,17_POPS,18_POPS,19_POPsS,20_POPS,21_POPS,22_POPS,23_POPS,24_POPS,25_POPS"
    ]

    data = file_header + pops

    return data
