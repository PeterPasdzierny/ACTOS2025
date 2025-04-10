import re


def decode_mcpc(raw_file):
    with open(raw_file, "r") as f:
        data = f.readlines()

    data = [
        (
            line.split("*")[0],
            bytes.fromhex(line.split("*")[1]).replace(b"\x00", b"").decode("ascii"),
        )
        for line in data
    ]

    sli = [i for i, line in enumerate(data) if "concent" in line[1]]
    offset = sli[0]
    eli = [i for i, line in enumerate(data[sli[0] :]) if "\r\r" in line[1]]
    if len(sli) > len(eli):
        sli = sli[: len(eli)]
    sei = [(sli[i], eli[i]) for i in range(len(sli))]

    mcpc = []
    for s in sei:
        current = []
        current.append(data[s[0]][0])
        current.append(",")

        for i in range(s[0], s[1] + offset + 1):
            line = data[i][1]
            current.append(line)

        current = "".join(current)
        current = re.sub(r"[a-zA-Z\=\_]+", "", current)
        current = re.sub("\r+", "", current)
        current = re.sub(r"\s+", ",", current)
        current = re.sub(",$", "", current)
        mcpc.append(current)

    file_header = [f"MCPC_{i}," for i in range(1, 19)]
    file_header.insert(
        0,
        "DATETIME,",
    )
    file_header = ["".join(file_header)]
    file_header[0] = file_header[0].rstrip(",")

    data = file_header + mcpc

    return data
