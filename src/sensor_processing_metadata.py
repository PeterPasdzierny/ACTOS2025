from decoding_functions import *

sensor_info = {
    "abc00e": {
        "sensor_name": "PTB",
        "decode_function": decode_ptb,
    },
    "abc01e": {
        "sensor_name": "HMP",
        "decode_function": decode_hmp,
    },
    "abc02e": {
        "sensor_name": "IMAR",
        "decode_function": decode_imar,
    },
    # "abc03e": {
    #     "sensor_name": "SPARV",
    # },
    "abc04e": {
        "sensor_name": "STAP",
        "decode_function": decode_stap,
    },
    "abc05e": {
        "sensor_name": "POPS",
        "decode_function": decode_pops,
    },
    "abc06e": {
        "sensor_name": "MCPC",
        "decode_function": decode_mcpc,
    },
    "abc07e": {
        "sensor_name": "MSEMS",
        "decode_function": decode_msems,
    },
    "abc08e": {
        "sensor_name": "LICOR",
        "decode_function": decode_licor,
    },
    "abc09e": {
        "sensor_name": "SONIC",
        "decode_function": decode_sonic,
    },
    "abc10e": {
        "sensor_name": "CDP",
    },
    "abc11e": {
        "sensor_name": "LWC",
        "decode_function": decode_lwc,
    },
    "abc12e": {
        "sensor_name": "CPCI",
        "decode_function": decode_cpc_I,
    },
    "abc13e": {
        "sensor_name": "CPCII",
        "decode_function": decode_cpc_II,
    },
    "abc14e": {
        "sensor_name": "AERORH",
        "decode_function": decode_aerorh,
    },
    "def0": {
        "sensor_name": "PTB",
    },
    "def1": {
        "sensor_name": "HMP",
    },
    "def2": {
        "sensor_name": "CPCS",
    },
    "def3": {
        "sensor_name": "PVMLWCPSA",
        "decode_function": decode_pvm,
    },
    "def4": {
        "sensor_name": "DPTT",
        "decode_function": decode_dptt,
    },
    "def5": {
        "sensor_name": "HOUSEKEEP",
        # "decode_function": decode_housekeep,
    },
    "def6": {
        "sensor_name": "RAD",
        # "decode_function": decode_rad,
    },
    "def7": {
        "sensor_name": "LICOR",
        # "decode_function": decode_licor,
    },
}
