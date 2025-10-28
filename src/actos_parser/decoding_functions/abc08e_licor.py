import re


def decode_licor(raw_file):
    with open(raw_file, "r") as f:
        data = f.readlines()

    data = [
        (
            line.split("*")[0],
            bytes.fromhex(line.split("*")[1][20:])
            .replace(b"\x00", b"")
            .decode("ascii"),
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
        current = re.sub(r"TRUE", "1", current)
        current = re.sub(r"FALSE", "0", current)
        current = re.sub(r"CO2", "", current)
        current = re.sub(r"H2O", "", current)
        current = re.sub(r"[\(\)]", ",", current)
        current = re.sub(r"(?<!\d{2})\s+(?!\d{2}:\d{2}:)", ",", current)
        current = re.sub(r"(?<!\d)e\-?(?!\d)", ",", current)
        current = re.sub(r"[a-df-zA-Z]", ",", current)
        current = re.sub(r"\,+", ",", current)
        current = re.sub(r"\,$", "", current)
        licor.append(current)

    file_header = [
        "DATETIME,NDX,DIAGVAL,CO2_RAW,CO2_D,H2O_RAW,H2O_D,TEMP,PRES,AUX,COOLER,SYNC,PLL,DET_OK,CHOPPER,PATH"
    ]

    data = file_header + licor

    return data
