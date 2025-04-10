import re


def decode_sonic(raw_file):
    with open(raw_file, "r") as f:
        data = f.readlines()

    data = [
        (
            line.split("*")[0],
            bytes.fromhex(line.split("*")[1])
            .replace(b"\x00", b"")
            .replace(b"\x0a", b"")
            .replace(b"\x0d", b"")
            .decode("ascii"),
        )
        for line in data
    ]
    sonic = [(data[i][0] + "," + data[i][1]) for i, _ in enumerate(data)]

    file_header = ["DATETIME,SONIC_1,SONIC_2,SONIC_3,SONIC_4,SONIC_5,SONIC_6,SONIC_7"]

    data = file_header + sonic

    return data
