import re


def decode_aerorh(raw_file):
    with open(raw_file, "r") as f:
        data = f.readlines()

    data = [
        (
            line.split("*")[0],
            bytes.fromhex(line.split("*")[1][20:])
            .replace(b"\x00", b"")
            .replace(b"\x0a", b"")
            .replace(b"\x09", b"\x2c")
            .decode("ascii"),
        )
        for line in data
    ]

    aerorh = [(data[i][0] + "," + data[i][1]) for i, _ in enumerate(data)]

    file_header = [
        "DATETIME,DATETIME_AERORH,AERORH_1,AERORH_PRESSURE,AERORH_3,AERORH_4,AERORH_5,AERORH_6,AERORH_7,AERORH_8,AERORH_9"
    ]

    data = file_header + aerorh

    return data
