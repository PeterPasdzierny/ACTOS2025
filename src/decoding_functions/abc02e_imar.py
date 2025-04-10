import datetime
import os
import numpy as np
import re
from struct import unpack


def gps_to_datetime(gps_week, tow_seconds, tow_fraction):
    gps_epoch = datetime.datetime(1980, 1, 6)
    tow_microseconds = tow_fraction
    timestamp_seconds = tow_seconds + tow_microseconds * 1e-6
    delta = datetime.timedelta(weeks=gps_week, seconds=timestamp_seconds)
    return gps_epoch + delta


def decode_insposllh(payload_range):
    insposllh = payload_range
    gps_week = int.from_bytes(insposllh[6:8], byteorder="little", signed=False)
    tow_seconds = int.from_bytes(insposllh[8:12], byteorder="little", signed=False)
    tow_fraction = int.from_bytes(insposllh[12:16], byteorder="little", signed=False)
    datetime_gps = gps_to_datetime(gps_week, tow_seconds, tow_fraction)
    lon = float(np.rad2deg(unpack("<d", insposllh[16:24])[0]))
    lat = float(np.rad2deg(unpack("<d", insposllh[24:32])[0]))
    height = unpack("<f", insposllh[32:36])[0]
    status_insposllh = int.from_bytes(
        insposllh[36:38], byteorder="little", signed=False
    )
    return f"{datetime_gps},{lon},{lat},{height},{status_insposllh}"


def decode_imucomp(payload_range):
    imucomp = payload_range
    acc_x, acc_y, acc_z = unpack("<3f", imucomp[16:28])
    omg_x, omg_y, omg_z = np.rad2deg(unpack("<3f", imucomp[28:40]))
    status_imucomp = int.from_bytes(imucomp[40:42], byteorder="little", signed=False)
    return f"{acc_x},{acc_y},{acc_z},{float(omg_x)},{float(omg_y)},{float(omg_z)},{status_imucomp}"


def decode_insrpy(payload_range):
    insrpy = payload_range
    roll, pitch, yaw = unpack("<3f", insrpy[16:28])
    status_insrpy = int.from_bytes(insrpy[28:30], byteorder="little", signed=False)
    return f"{roll},{pitch},{yaw},{status_insrpy}"


def decode_insvelbody(payload_range):
    insvelbody = payload_range
    v_x = unpack("<f", insvelbody[16:20])[0]
    v_y = unpack("<f", insvelbody[20:24])[0]
    v_z = unpack("<f", insvelbody[24:28])[0]
    status_insvelbody = int.from_bytes(
        insvelbody[28:30], byteorder="little", signed=False
    )
    return f"{v_x},{v_y},{v_z},{status_insvelbody}"


def decode_gnsssol(payload_range):
    gnsssol = payload_range
    lon = float(np.rad2deg(unpack("<d", gnsssol[16:24])[0]))
    lat = float(np.rad2deg(unpack("<d", gnsssol[24:32])[0]))
    altitude = unpack("<f", gnsssol[32:36])[0]
    v_north, v_east, v_down = np.rad2deg(unpack("<3f", gnsssol[40:52]))
    status_gnsssol = int.from_bytes(gnsssol[100:102], byteorder="little", signed=False)
    return f"{lon},{lat},{altitude},{float(v_north)},{float(v_east)},{float(v_down)},{status_gnsssol}"


def decode_imar(raw_file):
    with open(raw_file, "r") as f:
        data = f.readlines()

    data = [[line.split("*")[0], line.split("*")[1]] for line in data]

    testi = []
    for i, line in enumerate(data):
        old = line[1]
        new = line[1].rstrip("\n")
        if new.endswith("000000"):
            new = new[:-6]
        elif new.endswith("0000"):
            new = new[:-4]
        elif new.endswith("00"):
            new = new[:-2]
        else:
            new = new
        testi.append([line[0], new + "\n"])
    data = testi

    for i, line in enumerate(data):
        match = re.search(r"7e0a.{4}2800", line[1])
        if match:
            if match.start() == 0:
                data = data[i:]
                break

    data_new = []
    for i, line in enumerate(data):
        message_ranges = [m for m in re.finditer(r"7e0a.{4}2800", line[1])]
        if len(message_ranges) != 0:
            if message_ranges[0].start() == 0:
                data_new.append(data[i][0])
                data_new.append(data[i][1].rstrip("\n"))
            if message_ranges[0].start() != 0:
                rest_of_prev_line = data[i][1][: message_ranges[0].start()].rstrip("\n")
                current_line = data[i][1][message_ranges[0].start() :].rstrip("\n")
                data_new.append(rest_of_prev_line)
                data_new.append(data[i][0])
                data_new.append(current_line)
        else:
            rest_of_prev_line = data[i][1].rstrip("\n")
            data_new.append(rest_of_prev_line)

    data_new2 = []
    timestamp = ""
    text = ""
    for line in data_new:
        if "-" in line:
            if timestamp:
                data_new2.append(f"{timestamp},{text}")
                text = ""
                timestamp = line
            else:
                timestamp = line
        else:
            text += line
    if text:
        data_new2.append(f"{timestamp},{text}\n")

    inu_data = []
    for nr, line in enumerate(data_new2):
        timestamp = line.split(",")[0]
        inu_data.append(timestamp)
        datasection = line.split(",")[1]

        match = re.search(r"(7e0a.{4}2800)", datasection)
        if match:
            insposllh = datasection[match.start(1) : match.start(1) + 80]
            insposllh = decode_insposllh(bytes.fromhex(insposllh))
            inu_data.append(insposllh)
        else:
            inu_data.append("NAN,")

        match = re.search(r"(7e02.{4}2c00)", datasection)
        if match:
            imucomp = datasection[match.start(1) : match.start(1) + 88]
            imucomp = decode_imucomp(bytes.fromhex(imucomp))
            inu_data.append(imucomp)
        else:
            inu_data.append("NAN,")

        match = re.search(r"(7e04.{4}2000)", datasection)
        if match:
            insrpy = datasection[match.start(1) : match.start(1) + 64]
            insrpy = decode_insrpy(bytes.fromhex(insrpy))
            inu_data.append(insrpy)
        else:
            inu_data.append("NAN,")

        match = re.search(r"(7e09.{4}2000)", datasection)
        if match:
            insvelbody = datasection[match.start(1) : match.start(1) + 64]
            insvelbody = decode_insvelbody(bytes.fromhex(insvelbody))
            inu_data.append(insvelbody)
        else:
            inu_data.append(",NAN,")

        # NOT YET IMPLEMENTED CORRECTLY:
        # match = re.search(r"(7e12.{4}6800)", datasection)
        # if match:
        #     gnsssol = datasection[match.start(1) : match.start(1) + 208]
        #     gnsssol = decode_gnsssol(bytes.fromhex(gnsssol))
        # else:
        #     inu_data.append("NAN,")

    data_new5 = []
    timestamp = ""
    text = ""
    for line in inu_data:
        if "2000-01-" in line:
            if timestamp:
                data_new5.append(f"{timestamp},{text}")
                text = ""
                timestamp = line
            else:
                timestamp = line
        else:
            text += line
    if text:
        data_new5.append(f"{timestamp},{text}")

    data = data_new5

    return data
