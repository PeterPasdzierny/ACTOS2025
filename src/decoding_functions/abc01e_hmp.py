import re


def decode_hmp(raw_file):
    with open(raw_file, "r") as f:
        data = f.readlines()

    data = [
        (
            line.split("*")[0],
            bytes.fromhex(line.split("*")[1]).replace(b"\x00", b"").decode("ascii"),
        )
        for line in data
    ]

    sli = [i for i, line in enumerate(data) if "HMP" in line[1]]
    offset = sli[0]
    # eli = [i for i in sli[1:]]
    eli = [i for i, line in enumerate(data[sli[0] :]) if "\n" in line[1]]
    if len(sli) > len(eli):
        sli = sli[: len(eli)]
    sei = [(sli[i], eli[i]) for i in range(len(sli))]

    hmp = []
    for s in sei:
        current = []
        current.append(data[s[0]][0])

        for i in range(s[0], s[1] + offset + 1):
            line = re.sub(r"[HMP]", "", data[i][1].rstrip())
            line = re.sub(r"[^\d\.\-\s]", "", line)
            line = re.sub(r"\s+", ",", line)
            current.append(line)

        current = "".join(current)
        hmp.append(current)

    file_header = ["DATETIME,1_HMP,2_HMP,3_HMP"]

    data = file_header + hmp

    return data
