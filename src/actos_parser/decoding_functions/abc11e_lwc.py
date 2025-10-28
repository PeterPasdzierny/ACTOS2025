import re


def decode_lwc(raw_file):
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

    sli = [i for i, line in enumerate(data) if "$Fin" in line[1] and len(line[1]) > 50]
    eli = [
        i
        for i, line in enumerate(data)
        if re.search(r"\.\d{5}\,[A-Z0-9]{4}\n$", line[1]) and len(line[1]) > 50
    ]
    if eli[0] < sli[0]:
        eli = eli[1:]
    if len(sli) > len(eli):
        sli = sli[: len(eli)]
    sei = [(sli[i], eli[i]) for i in range(len(sli))]

    lwc = []
    for s in sei:
        current = []
        current.append(data[s[0]][0])
        current.append(",")
        for i in range(s[0], s[1] + 1):
            line = re.sub(r"\$Fin-\d{1},", "", data[i][1])
            line = re.sub("\n", "", line)
            current.append(line)
        current = "".join(current)
        lwc.append(current)

    file_header = [f"LWC_{i}" for i in range(1, 51)]
    file_header.insert(0, "DATETIME")
    file_header = [",".join(file_header)]

    data = file_header + lwc

    return data
