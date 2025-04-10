import re


def decode_msems(raw_file):
    with open(raw_file, "r") as f:
        data = f.readlines()

    data = [
        (
            line.split("*")[0],
            bytes.fromhex(line.split("*")[1]).replace(b"\x00", b"").decode("ascii"),
        )
        for line in data
    ]

    sli = [i for i, line in enumerate(data) if re.match("^sheath_rh=", line[1])]
    offset = sli[0]
    eli = [i for i in sli[1:]]
    if len(sli) > len(eli):
        sli = sli[: len(eli)]
    sei = [(sli[i], eli[i]) for i in range(len(sli))]

    msems = []
    for s in sei:
        current = []
        current.append(data[s[0]][0])

        for i in range(s[0], s[1] + offset):
            line = data[i][1]
            current.append(line)

        current = "".join(current)
        current = re.sub(r"[a-zA-Z\=\_]+", ",", current)
        current = re.sub("\r+", "", current)
        current = re.sub("\n", "", current)

        current = current.split(",")
        if len(current) > 25:
            current = ",".join(current[:-23])
            current = current.split(",")
            current = current[:24] + current[26:]
            current = ",".join(current)
        elif len(current) == 25:
            current = ",".join(current)
            current += "," * 141
        elif len(current) == 24:
            current = ",".join(current)
            current += "," * 142

        msems.append(current)

    file_header = [f"MSEMS_{i}," for i in range(1, 167)]
    file_header.insert(
        0,
        "DATETIME,",
    )
    file_header = ["".join(file_header)]
    file_header[0] = file_header[0].rstrip(",")

    data = file_header + msems

    return data
