import re


def decode_msems(raw_file):
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

    sli = [i for i, line in enumerate(data) if re.match("sheath_rh=", line[1])]
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
        current += ""
        current = re.sub(r"[a-zA-Z\=\_]+", ",", current)
        current = re.sub("\r+", "", current)
        current = re.sub("\n", "", current)

        current_splits = current.split(",")
        if len(current_splits) > 24:
            current = ",".join(current_splits[:24])
            current += ","
            current += ";".join(current_splits[24:])
        elif len(current_splits) == 24:
            current = ",".join(current_splits[:24])
            current += ",-999"
        else:
            current = "ERRO_PARSING_THIS_MSEMS_LINE"

        msems.append(current)

    file_header=["DATETIME,SHEATH_RH,SHEATH_TEMP,PRESSURE,LFE_TEMP,SHEATH_FLOW,SHEATH_PWR,IMPPRS,HV_VOLTS,HV_DAC,SD_INSTALL,EXT_VOLTS,MSEMS_ERRS,MCPC_HRTB,MCPC_SMPF,MCPC_SATF,MCPC_CNDT,MCPC_SATT,MCPC_SN,MCPC_ERRS,MCPCPWR,MCPCPMP,SD_SAVE,SAVE_FLAG,SCAN_DATA"]

    data = file_header + msems

    return data
