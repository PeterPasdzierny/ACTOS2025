import re


def decode_sonic(raw_file):
    with open(raw_file, "r") as f:
        data = f.readlines()

    data = [
        (
            line.split("*")[0],
            bytes.fromhex(line.split("*")[1][20:])
            .replace(b"\x00", b"")
            .replace(b"\x0a", b"")
            .replace(b"\x0d", b"")
            .decode("ascii"),
        )
        for line in data
    ]
    sonic = [(data[i][0] + "," + data[i][1]) for i, _ in enumerate(data)]

    file_header = [
        "DATETIME,SONIC_U,SONIC_V,SONIC_W,SONIC_T,SONIC_STATUS,SONIC_COUNTER,SONIC_CHECKSUM"
    ]

    data = file_header + sonic

    return data
