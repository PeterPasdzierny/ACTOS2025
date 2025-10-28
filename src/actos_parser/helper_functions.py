import argparse
from datetime import datetime, timedelta
import dpkt
from os import listdir, mkdir
from os.path import exists, isdir, join
import shutil


pcap_subdir = "l0_pcap/"
raw_subdir = "l1a_raw_data/"
decoded_subdir = "l1_decoded_data/"


def get_flightdirectory():
    path_parser = argparse.ArgumentParser()
    path_parser.add_argument("path")
    flightdir = path_parser.parse_args()
    return flightdir.path


def get_pcap_list(pcap_file):
    pcap_reader = dpkt.pcap.Reader(open(pcap_file, "rb"))
    pcap_list = [packet for packet in sorted(pcap_reader)]
    return pcap_list


def convert_pcap_timestamp(pcap_timestamp):
    return datetime.fromtimestamp(pcap_timestamp)


def get_sequence_nr(packet):
    return int(packet[50:54].hex(), 16)


def get_ptp(packet):
    ptp_seconds = datetime.fromtimestamp(int(packet[58:62].hex(), 16))
    ptp_microseconds = int(packet[62:66].hex(), 16) / 1000
    ptp = ptp_seconds + timedelta(microseconds=ptp_microseconds)
    ptp = datetime.strftime(ptp, "%Y-%m-%d %H:%M:%S.%f")
    return ptp


def get_payload(packet):
    # return packet[70 + 10 :]
    return packet[70:]


# def get_payload_def(packet):
#     return packet[70:]


def get_stream_id(packet):
    return packet[46:50].hex().lstrip("0")


def get_flightfiles(flightdir):
    flightfiles = [
        join(flightdir, pcap_subdir, pcap_file)
        for pcap_file in sorted(listdir(join(flightdir, pcap_subdir)))
    ]
    return flightfiles


def get_l1a_raw_files(flightdir):
    raw_files = [
        join(flightdir, raw_subdir, raw_file)
        for raw_file in sorted(listdir(join(flightdir, raw_subdir)))
    ]
    return raw_files


def get_l1_decoded_files(flightdir):
    raw_files = [
        join(flightdir, decoded_subdir, decoded_file)
        for decoded_file in sorted(listdir(join(flightdir, decoded_subdir)))
    ]
    return raw_files


def sort_l1a_raw_files_by_timestamp(raw_files):
    for raw_file in raw_files:
        with open(raw_file, "r") as infile:
            data = infile.readlines()
        data = sorted(data)
        with open(raw_file, "w") as outfile:
            [outfile.write(line) for line in data]


def create_l1a_raw_subdir(flightdir):
    outdir = join(flightdir, raw_subdir)
    # if isdir(outdir):
    #     shutil.rmtree(outdir)
    if not exists(outdir):
        mkdir(outdir)


def create_l1_decoded_subdir(flightdir):
    outdir = join(flightdir, decoded_subdir)
    # if isdir(outdir):
    #     shutil.rmtree(outdir)
    if not exists(outdir):
        mkdir(outdir)


def write_l1a_raw_data(flightdir, stream_id, sensor_name, ptp, payload):
    outpath = f"{flightdir}{raw_subdir}{stream_id}_{sensor_name}.txt"
    with open(outpath, "a") as outfile:
        outfile.write(f"{ptp}*{str(payload)}\n")


def write_l1_decoded_data(flightdir, raw_file, data):
    outpath = f"{flightdir}{decoded_subdir}{raw_file.split('/')[-1].split('.')[0]}.txt"
    with open(outpath, "w") as outfile:
        [outfile.write(line + "\n") for line in data]
