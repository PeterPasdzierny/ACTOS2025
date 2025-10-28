import re


def decode_mcpc(raw_file):
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
        current = re.sub(r"(?<!-\d{2}-\d{2})\s+(?!\d{2}:\d{2}:)", ",", current)
        current = re.sub(",$", "", current)
        mcpc.append(current)

    file_header = ["DATETIME,CONCENT,RAWCONC,CNT_SEC,CONDTMP,SATTTMP,SATBTMP,OPTCTMP,INLTTMP,SMPFLOW,SATFLOW,PRESSUR,CONDPWR,SATTPWR,SATBPWR,OPTCPWR,SATFPWR,FILLCNT,ERR_NUM"]

    data = file_header + mcpc

    return data
