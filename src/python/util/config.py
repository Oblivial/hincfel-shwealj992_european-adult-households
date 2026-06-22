import json 

config = None

def loadConfig():
    global config
    with open("src/config.json", "r") as f:
        config = json.load(f)

def getWIDFolderPath():
    if not config:
        loadConfig()
    return config["wid_folder"]

def getESSFolderPath():
    if not config:
        loadConfig()
    return config["ess_folder"]

def getOutputFolderPath():
    if not config:
        loadConfig()
    return config["output_folder"]