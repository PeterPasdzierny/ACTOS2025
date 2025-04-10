# import re
#
#
# def decode_housekeep(raw_file):
#     with open(raw_file, "r") as f:
#         data = f.readlines()
#     # print(data)
#
#     # data = [
#     #     (
#     #         line.split("*")[0],
#     #         bytes.fromhex(line.split("*")[1]),
#     #     )
#     #     for line in data
#     # ]
#
#     for i, line in enumerate(data):
#         lwc1 = int(line.split("*")[1][:4], 16)
#         lwc2 = int(line.split("*")[1][4:8], 16)
#         psa1 = int(line.split("*")[1][8:12], 16)
#         psa2 = int(line.split("*")[1][12:], 16)
#
#         lwc1 = lwc1 / 2**16 * 5
#         lwc2 = lwc2 / 2**16 * 5
#         psa1 = psa1 / 2**16 * 5
#         psa2 = psa2 / 2**16 * 5
#
#         print(lwc1, psa1)
#
#     # pvm = [(data[i][0] + "," + data[i][1]) for i, _ in enumerate(data)]
#
#     # file_header = [
#     #     "DATETIME,AERORH_1,AERORH_2,AERORH_3,AERORH_4,AERORH_5,AERORH_6,AERORH_7,AERORH_8,AERORH_9"
#     # ]
#     #
#     # data = file_header + pvm
#     #
#     # return data
