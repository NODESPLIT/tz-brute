from pathlib import Path
import datetime
import json
import os

data = {
	"parameters" : {
		"charset" : 4,
		"custom" : "",
		"minimum" : 3,
		"chunk" : 100
	},
	"details" : {
		"address" : "",
		"email" : "",
		"mnemonic" : ""
	},
	"status" : {
		"success" : False,
		"length" : 3,
		"depth" : 0
	}
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