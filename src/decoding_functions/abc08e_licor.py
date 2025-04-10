import re


def decode_licor(raw_file):
    with open(raw_file, "r") as f:
        data = f.readlines()

    data = [
        (
            line.split("*")[0],
            bytes.fromhex(line.split("*")[1]).replace(b"\x00", b"").decode("ascii"),
        )
        for line in data
    ]

    sli = [i for i, line in enumerate(data) if "(Data (" in line[1]]
    offset = sli[0]
    eli = [i for i in sli[1:]]
    if len(sli) > len(eli):
        sli = sli[: len(eli)]
    sei = [(sli[i], eli[i]) for i in range(len(sli))]

    licor = []
    for s in sei:
        current = []
        current.append(data[s[0]][0])
        current.append(",")

        for i in range(s[0], s[1] + offset):
            line = data[i][1]
            current.append(line)

        current = "".join(current)
        current = re.sub("[\r+\n+]", "", current)
        current = re.sub("\)\)", ")", current)
        current = re.sub("Data \(", "", current)
        current = re.sub("Diagnostics \(", "", current)
        current = re.sub("\(", ";", current)
        current = re.sub("\)", ";", current)
        # current = re.sub(r"[(a-z)+(A_Z)+] ?\d", "", current)

        licor.append(current)

    file_header = [f"LICOR_{i}," for i in range(1, 19)]
    file_header.insert(
        0,
        "DATETIME,",
    )
    file_header = ["".join(file_header)]
    file_header[0] = file_header[0].rstrip(",")

    data = file_header + licor

    return data
