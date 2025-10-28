from helper_functions import *
import pandas as pd
from sensor_processing_metadata import sensor_info


def main():
    # flightdir = get_flightdirectory()
    flightdirs = [
        # "../data/20250407_RF01/",
        # "../data/20250408_RF02/",
        # "../data/20250409_RF03/",
        # "../data/20250411_RF04/",
        # "../data/20250412_RF05/",
        # "../data/20250414_RF06/",
        # "../data/20250414_RF07/",
        # "../data/20250415_RF08/",
        # "../data/20250417_RF09/",
        # "../data/20250418_RF10/",
        # "../data/20250419_RF11/",
        # "../data/20250422_RF12/",
        # "../data/20250426_RF13/",
        "../data/20250426_RF14/",
    ]

    for flightdir in flightdirs:
        print("TEST")
        #     flightfiles = get_flightfiles(flightdir)
        #     create_l1a_raw_subdir(flightdir)
        #
        #     print(f"Start processing of flight {flightdir.split('/')[-2]}...")
        #
        #     for nr, file in enumerate(flightfiles):
        #         pcap_list = get_pcap_list(file)
        #
        #         print(f"Processing pcapfile {nr + 1} of {len(flightfiles)}")
        #
        #         for _, packet in pcap_list:
        #             # pcap_timestamp = convert_pcap_timestamp(pcap_timestamp)
        #             stream_id = get_stream_id(packet)
        #             # seq_number = get_sequence_nr(packet)
        #             ptp = get_ptp(packet)
        #             # if "def" in stream_id:
        #             #     payload = get_payload_def(packet)
        #             # else:
        #             payload = get_payload(packet)
        #
        #             if stream_id in sensor_info.keys():
        #                 sensor_name = sensor_info[stream_id]["sensor_name"]
        #                 write_l1a_raw_data(
        #                     flightdir, stream_id, sensor_name, ptp, payload.hex()
        #                 )
        #             else:
        #                 # print(f"Stream-ID {stream_id} is not known! Skipping package...")
        #                 continue
        #
        #     raw_files = get_l1a_raw_files(flightdir)
        #     create_l1_decoded_subdir(flightdir)
        #     sort_l1a_raw_files_by_timestamp(raw_files)
        #
        #     for raw_file in raw_files:
        #         stream_id = raw_file.split("/")[-1].split("_")[0]
        #         # if stream_id == "abc00e":
        #         print(f"Decoding {stream_id} raw-data file...")
        #         if "decode_function" in sensor_info[stream_id].keys():
        #             try:
        #                 data = sensor_info[stream_id]["decode_function"](raw_file)
        #                 write_l1_decoded_data(flightdir, raw_file, data)
        #             except Exception as e:
        #                 print(f"Processing of {stream_id} raw file failed. Skipping file...")
        #                 print(e)
        #         else:
        #             print(
        #                 f"No parser for stream-ID: {stream_id} implemented yet. Skipping file..."
        #             )
        #
        #     imar_file = f"{flightdir}/{decoded_subdir}/abc02e_IMAR.txt"
        #     imar_df = pd.read_csv(
        #         imar_file,
        #         header=0,
        #         parse_dates=[0, 1],
        #         date_format="ISO8601",
        #         dayfirst=False,
        #         usecols=[0, 1],
        #     )
        #     current_flight_datetime_offset = (imar_df.DATETIME_GPS - imar_df.DATETIME)[0]
        #
        #     not_yet_fixed_stream_ids = [
        #         # "abc00",
        #         # "abc01",
        #         "abc02",
        #         # "abc03",
        #         # "abc04",
        #         # "abc05",
        #         # "abc06",
        #         # "abc07",
        #         # "abc08",
        #         # "abc09",
        #         # "abc10",
        #         # "abc11",
        #         # "abc12",
        #         # "abc13",
        #         # "abc14",
        #         # "def2",
        #         # "def3",
        #         # "def4",
        #         # "def5",
        #         # "def6",
        #         # "def7",
        #     ]
        #     decoded_files = get_l1_decoded_files(flightdir)
        #     for decoded_file in decoded_files:
        #         try:
        #             if all(i not in decoded_file for i in not_yet_fixed_stream_ids):
        #                 df = pd.read_csv(
        #                     decoded_file,
        #                     header=0,
        #                     parse_dates=[0],
        #                     date_format="ISO8601",
        #                     dayfirst=False,
        #                     na_values=-999,
        #                     low_memory=False,
        #                 )
        #                 df["DATETIME"] += current_flight_datetime_offset
        #                 df.to_csv(decoded_file, index=False, na_rep="-999")
        #         except Exception as e:
        #             print(e)

        print(f"Processing of {flightdir.split('/')[-2]} complete!")


if __name__ == "__main__":
    main()
