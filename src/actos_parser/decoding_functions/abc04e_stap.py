import re


def decode_stap(raw_file):
    with open(raw_file, "r") as f:
        data = f.readlines()

    data = [
        (
            line.split("*")[0],
            bytes.fromhex(line.split("*")[1][20:])
            .replace(b"\x00", b"")
            .replace(b"\x09", b"")
            .replace(b"\x0d", b"")
            .decode("ascii"),
        )
        for line in data
    ]

    if not "." in data[0][1][:7]:
        data = data[1:]

    timestamps = [data[i][0] for i, _ in enumerate(data)]

    stap_1 = data[0::2]
    stap_2 = data[1::2]

    data_1 = [(re.sub(r"\s+", ",", stap_1[i][1])) for i, _ in enumerate(stap_1)]
    data_2 = [(re.sub(r"\s+", ",", stap_2[i][1])) for i, _ in enumerate(stap_2)]

    data_1 = [data_1[i] for i, _ in enumerate(data_1)]
    data_1 = [re.sub(r"\,", ",,", data_1[i]) for i, _ in enumerate(data_1)]
    data_1 = [re.sub("^", ",", data_1[i]) for i, _ in enumerate(data_1)]
    data_1 = [re.sub(",,$", ",", data_1[i]) for i, _ in enumerate(data_1)]

    data_2 = [data_2[i] for i, _ in enumerate(data_2)]
    data_2 = [re.sub(r"\,", ",,", data_2[i]) for i, _ in enumerate(data_2)]
    data_2 = [re.sub(",,$", "", data_2[i]) for i, _ in enumerate(data_2)]
    data = [i for pair in zip(data_1, data_2) for i in pair]

    stap = [(timestamps[i] + "," + data[i]) for i, _ in enumerate(data)]

    file_header = [
        "DATETIME,1_STAP,2_STAP,3_STAP,4_STAP,5_STAP,6_STAP,7_STAP,8_STAP,9_STAP,10_STAP,11_STAP,12_STAP,13_STAP,14_STAP,15_STAP,16_STAP,17_STAP,18_STAP,19_STAP"
    ]

    data = file_header + stap

    return data
