from sensor_processing_metadata import sensor_info
from helper_functions import *


flightdir = get_flightdirectory()
# flightdir = f"../data/20250409_RF03/"
flightfiles = get_flightfiles(flightdir)
create_raw_subdir(flightdir)

print(f"Start processing of flight {flightdir.split('/')[-2]}...")

for nr, file in enumerate(flightfiles):
    pcap_list = get_pcap_list(file)

    print(f"Processing pcapfile {nr + 1} of {len(flightfiles)}")

    for _, packet in pcap_list:
        # pcap_timestamp = convert_pcap_timestamp(pcap_timestamp)
        stream_id = get_stream_id(packet)
        # seq_number = get_sequence_nr(packet)
        ptp = get_ptp(packet)
        if "def" in stream_id:
            payload = get_payload_def(packet)
        else:
            payload = get_payload(packet)

        if stream_id in sensor_info.keys():
            sensor_name = sensor_info[stream_id]["sensor_name"]
            write_raw_data(flightdir, stream_id, sensor_name, ptp, payload.hex())
        else:
            print(f"Stream-ID {stream_id} is not known! Skipping package...")
            continue


raw_files = get_raw_files(flightdir)
create_decoded_subdir(flightdir)
sort_raw_files_by_timestamp(raw_files)

for raw_file in raw_files:
    stream_id = raw_file.split("/")[-1].split("_")[0]

    print(f"Decoding {stream_id} raw-data file...")

    if "decode_function" in sensor_info[stream_id].keys():
        data = sensor_info[stream_id]["decode_function"](raw_file)
        write_decoded_data(flightdir, raw_file, data)
    else:
        print(f"No parser for stream-ID: {stream_id} implemented yet. Skipping file...")


print(f"Processing of {flightdir.split('/')[-2]} complete!")
