import re


def decode_cpc_I(raw_file):
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

    cpc_I = [(data[i][0] + "," + data[i][1]) for i, _ in enumerate(data)]

    file_header = ["DATETIME,CPC_I"]

    data = file_header + cpc_I

    return data
