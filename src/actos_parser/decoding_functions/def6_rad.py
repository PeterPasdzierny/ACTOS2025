import re


def decode_rad(raw_file):
    with open(raw_file, "r") as f:
        data = f.readlines()

    rad = []
    for line in data:
        ptp, data = line.split("*")

        rad1 = int(data[:4], 16)
        rad2 = int(data[4:8], 16)
        rad3 = int(data[8:12], 16)
        rad4 = int(data[12:16], 16)
        rad5 = int(data[16:20], 16)
        rad6 = int(data[20:24], 16)

        u_cgr4_down = rad1 / 2**16 * 0.04 - 0.02
        u_cgr4_down_t = rad2 / 2**16 * 20 - 10
        u_cgr4_up = rad3 / 2**16 * 0.04 - 0.02
        u_cgr4_up_t = rad4 / 2**16 * 20 - 10
        u_cmp22_down = rad5 / 2**16 * 0.04 - 0.02
        u_cmp22_up = rad5 / 2**16 * 0.04 - 0.02

        cgr4_down = u_cgr4_down / 11.67e-6
        cgr4_down_t = u_cgr4_down_t * 1e3
        cgr4_up = u_cgr4_up / 11.03e-6
        cgr4_up_t = u_cgr4_up_t * 1e3
        cmp22_down = u_cmp22_down / 9.19e-6
        cmp22_up = u_cmp22_up / 9.14e-6

        rad.append(
            f"{ptp},{cgr4_down},{cgr4_down_t},{cgr4_up},{u_cgr4_up_t},{cmp22_down},{cmp22_up}"
        )

    file_header = [
        "DATETIME,CGR4_DOWN,CGR4_DOWN_T,CGR4_UP,CGR4_UP_T,CMP22_DOWN,CMP22_UP"
    ]

    data = file_header + rad

    return data
