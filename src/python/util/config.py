import json 

config = None

def load_config():
    global config
    with open("src/config.json", "r") as f:
        config = json.load(f)

def get_wid_folderpath():
    if not config:
        load_config()
    return config["wid_folder"]

def get_ess_folderpath():
    if not config:
        load_config()
    return config["ess_folder"]

def get_output_folderpath():
    if not config:
        load_config()
    return config["output_folder"]

def get_ess_rounds():
    if not config:
        load_config()
    return config["ess_round_dates"]