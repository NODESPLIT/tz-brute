import sys

import anchor
import brute
import tezos

charsets = [
	"0123456789",
	"0123456789abcdefghijklmnopqrstuvwxyz",
	"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
	"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
	"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&'()*+,-./:;<=>?@[\]^_`{|}~",
	"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
]


if len(sys.argv) > 1 and sys.argv[1] == "reset":
	anchor.reset()
	sys.exit()

if anchor.exists():
	anchor.load()
	charsets.append(anchor.data["parameters"]["custom"])
	if anchor.data["status"]["success"]:
		print("Password is {}. Found in {} guesses at a length of {}.".format(anchor.data["status"]["match"], anchor.data["status"]["depth"], anchor.data["status"]["length"]))
		sys.exit()
else:
	i = 1
	print("Charsets:")
	for charset in charsets:
		print("["+str(i)+"]: "+charset)
		i += 1
	print("["+str(i)+"]: CUSTOM CHARSET (ADVANCED)")

	selected_charset = "-1"
	while not (selected_charset.isdigit() and int(selected_charset) >= 1 and int(selected_charset) <= 7):
		selected_charset = input("Please select a charset (1 - 7): ")
	anchor.data["parameters"]["charset"] = int(selected_charset) - 1
	
	if anchor.data["parameters"]["charset"] == 6:
		selected_custom_charset = ""
		while len(selected_custom_charset) == 0:
			selected_custom_charset = input("Please enter a custom charset (e.g. 0123456789abcde...): ")
		anchor.data["parameters"]["custom"] = selected_custom_charset
		charsets.append(anchor.data["parameters"]["custom"])
	
	selected_minimum = "-1"
	while not (selected_minimum.isdigit() and int(selected_minimum) >= 6):
		selected_minimum = input("Please select a minimum length (6 - ?): ")
	anchor.data["parameters"]["minimum"] = int(selected_minimum)
	anchor.data["status"]["length"] = int(selected_minimum)
	
	selected_address = ""
	while len(selected_address) == 0:
		selected_address = input("Please enter your tezos contribution public key (e.g. tz1ABCDeF...): ")
	anchor.data["details"]["address"] = selected_address
	
	selected_email = ""
	while len(selected_email) == 0:
		selected_email = input("Please enter your tezos contribution email address (you can enter multiple by separating them with a comma): ")
	anchor.data["details"]["email"] = selected_email
	
	selected_mnemonic = ""
	while len(selected_mnemonic) == 0:
		selected_mnemonic = input("Please enter your tezos contribution mnemonic (e.g. apples cat radio...): ")
	anchor.data["details"]["mnemonic"] = selected_mnemonic

	anchor.save()


def cache(length, depth):
	anchor.data["status"]["length"] = length
	anchor.data["status"]["depth"] = depth
	anchor.save()

emails = anchor.data["details"]["email"].split(",")
mnemonic = anchor.data["details"]["mnemonic"].encode()

def check(password):
	global emails, mnemonic
	for email in emails:
		if tezos.check(anchor.data["details"]["address"], mnemonic, email, password) == 1:
			return True
	return False


charset = charsets[anchor.data["parameters"]["charset"]]
print("Starting bruteforce with charset[{}]...".format(charset))

password = brute.force([int(anchor.data["status"]["length"]), int(anchor.data["status"]["depth"])], charset, anchor.data["parameters"]["minimum"], 100, 1000, check, cache)
if password:
	print("\n\nGot it! Password is \"{}\"".format(password))
	anchor.data["status"]["match"] = password
	anchor.data["status"]["success"] = True
	anchor.save()