from datetime import datetime, timedelta
import re


def decode_licor_def(raw_file):
    with open(raw_file, "r") as f:
        data = f.readlines()

    licor = []
    for line in data:
        ptp1, data = line.split("*")
        try:
            ptp_temp = datetime.strptime(ptp1, "%Y-%m-%d %H:%M:%S.%f")
        except:
            ptp_temp = datetime.strptime(ptp1, "%Y-%m-%d %H:%M:%S")
        ptp2 = ptp_temp + timedelta(milliseconds=2)
        ptp3 = ptp_temp + timedelta(milliseconds=4)
        ptp4 = ptp_temp + timedelta(milliseconds=6)
        ptp5 = ptp_temp + timedelta(milliseconds=8)
        ptp6 = ptp_temp + timedelta(milliseconds=10)
        ptp7 = ptp_temp + timedelta(milliseconds=12)
        ptp8 = ptp_temp + timedelta(milliseconds=14)
        ptp9 = ptp_temp + timedelta(milliseconds=16)
        ptp10 = ptp_temp + timedelta(milliseconds=18)
        ptp2 = datetime.strftime(ptp2, "%Y-%m-%d %H:%M:%S.%f")
        ptp3 = datetime.strftime(ptp3, "%Y-%m-%d %H:%M:%S.%f")
        ptp4 = datetime.strftime(ptp4, "%Y-%m-%d %H:%M:%S.%f")
        ptp5 = datetime.strftime(ptp5, "%Y-%m-%d %H:%M:%S.%f")
        ptp6 = datetime.strftime(ptp6, "%Y-%m-%d %H:%M:%S.%f")
        ptp7 = datetime.strftime(ptp7, "%Y-%m-%d %H:%M:%S.%f")
        ptp8 = datetime.strftime(ptp8, "%Y-%m-%d %H:%M:%S.%f")
        ptp9 = datetime.strftime(ptp9, "%Y-%m-%d %H:%M:%S.%f")
        ptp10 = datetime.strftime(ptp10, "%Y-%m-%d %H:%M:%S.%f")

        co2_1 = int(data[0:4], 16)
        co2_2 = int(data[4:8], 16)
        co2_3 = int(data[8:12], 16)
        co2_4 = int(data[12:16], 16)
        co2_5 = int(data[16:20], 16)
        co2_6 = int(data[20:24], 16)
        co2_7 = int(data[24:28], 16)
        co2_8 = int(data[28:32], 16)
        co2_9 = int(data[32:36], 16)
        co2_10 = int(data[36:40], 16)
        h20_1 = int(data[40:44], 16)
        h20_2 = int(data[44:48], 16)
        h20_3 = int(data[48:52], 16)
        h20_4 = int(data[52:56], 16)
        h20_5 = int(data[56:60], 16)
        h20_6 = int(data[60:64], 16)
        h20_7 = int(data[64:68], 16)
        h20_8 = int(data[68:72], 16)
        h20_9 = int(data[72:76], 16)
        h20_10 = int(data[76:80], 16)

        co2_1 = co2_1 / 2**16 * 5
        co2_2 = co2_2 / 2**16 * 5
        co2_3 = co2_3 / 2**16 * 5
        co2_4 = co2_4 / 2**16 * 5
        co2_5 = co2_5 / 2**16 * 5
        co2_6 = co2_6 / 2**16 * 5
        co2_7 = co2_7 / 2**16 * 5
        co2_8 = co2_8 / 2**16 * 5
        co2_9 = co2_9 / 2**16 * 5
        co2_10 = co2_10 / 2**16 * 5
        h20_1 = h20_1 / 2**16 * 5
        h20_2 = h20_2 / 2**16 * 5
        h20_3 = h20_3 / 2**16 * 5
        h20_4 = h20_4 / 2**16 * 5
        h20_5 = h20_5 / 2**16 * 5
        h20_6 = h20_6 / 2**16 * 5
        h20_7 = h20_7 / 2**16 * 5
        h20_8 = h20_8 / 2**16 * 5
        h20_9 = h20_9 / 2**16 * 5
        h20_10 = h20_10 / 2**16 * 5

        licor.append(f"{ptp1},{h20_1},{co2_1}")
        licor.append(f"{ptp2},{h20_2},{co2_2}")
        licor.append(f"{ptp3},{h20_3},{co2_3}")
        licor.append(f"{ptp4},{h20_4},{co2_4}")
        licor.append(f"{ptp5},{h20_5},{co2_5}")
        licor.append(f"{ptp6},{h20_6},{co2_6}")
        licor.append(f"{ptp7},{h20_7},{co2_7}")
        licor.append(f"{ptp8},{h20_8},{co2_8}")
        licor.append(f"{ptp9},{h20_9},{co2_9}")
        licor.append(f"{ptp10},{h20_10},{co2_10}")

    file_header = ["DATETIME,LICOR_CO2,LICOR_H2O"]

    data = file_header + licor

    return data
