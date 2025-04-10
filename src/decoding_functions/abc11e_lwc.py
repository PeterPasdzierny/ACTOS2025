import re


def decode_lwc(raw_file):
    with open(raw_file, "r") as f:
        data = f.readlines()

    data = [
        (
            line.split("*")[0],
            bytes.fromhex(line.split("*")[1])
            .replace(b"\x00", b"")
            .replace(b"\x0d", b"")
            .decode("ascii"),
        )
        for line in data
    ]

    sli = [i for i, line in enumerate(data) if "$Fin" in line[1]]
    offset = sli[0]
    eli = [i for i, line in enumerate(data[sli[0] :]) if "\n" in line[1]]
    if len(sli) > len(eli):
        sli = sli[: len(eli)]
    sei = [(sli[i], eli[i]) for i in range(len(sli))]

    lwc = []
    for s in sei:
        current = []
        current.append(data[s[0]][0])
        current.append(",")

        for i in range(s[0], s[1] + offset + 1):
            line = re.sub(r"[$Fin]", "", data[i][1])
            line = re.sub("\n", "", line)
            current.append(line)

        current = "".join(current)
        lwc.append(current)

    file_header = [f"LWC_{i}," for i in range(1, 51)]
    file_header.insert(
        0,
        "DATETIME,",
    )
    file_header = ["".join(file_header)]
    file_header[0] = file_header[0].rstrip(",")

    data = file_header + lwc

    return data
