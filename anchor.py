from pathlib import Path
import datetime
import json
import os

data = {
	"parameters" : {
		"charset" : 4,
		"minimum" : 3
	},
	"details" : {
		"address" : "",
		"email" : "",
		"mnemonic" : "",
		"password" : ""
	},
	"success" : False,
	"depth" : 0
}

def exists():
	return Path("anchor.json").is_file()

def load():
	global data
	with open("anchor.json") as file:
		data = json.load(file)

def save():
	global data
	with open("anchor.json", "w") as file:
	    json.dump(data, file, indent=True)

def reset():
	if Path("anchor.json").is_file():
		os.rename("anchor.json", "anchor_backup_"+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+".json")