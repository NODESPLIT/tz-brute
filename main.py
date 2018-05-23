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
	if anchor.data["success"]:
		print("Password is {}. Found in {} guesses.".format(anchor.data["details"]["password"], anchor.data["depth"]))
		sys.exit()
else:
	i = 1
	print("Charsets:")
	for charset in charsets:
		print("["+str(i)+"]: "+charset)
		i += 1

	selected_charset = "-1"
	while not (selected_charset.isdigit() and int(selected_charset) >= 1 and int(selected_charset) <= 6):
		selected_charset = input("Please select a charset (1 - 6): ")
	anchor.data["parameters"]["charset"] = int(selected_charset) - 1
	
	selected_minimum = "-1"
	while not (selected_minimum.isdigit() and int(selected_minimum) >= 1):
		selected_minimum = input("Please select a minimum length (1 - ?): ")
	anchor.data["parameters"]["minimum"] = int(selected_minimum)
	
	selected_address = ""
	while len(selected_address) == 0:
		selected_address = input("Please enter your tezos contribution public key (e.g. tz1ABCDeF...): ")
	anchor.data["details"]["address"] = selected_address
	
	selected_email = ""
	while len(selected_email) == 0:
		selected_email = input("Please enter your tezos contribution email address: ")
	anchor.data["details"]["email"] = selected_email
	
	selected_mnemonic = ""
	while len(selected_mnemonic) == 0:
		selected_mnemonic = input("Please enter your tezos contribution mnemonic (e.g. apples cat radio...): ")
	anchor.data["details"]["mnemonic"] = selected_mnemonic

	anchor.save()


def cache(depth):
	anchor.data["depth"] = depth
	anchor.save()

def check(password):
	return tezos.check(anchor.data["details"]["address"], anchor.data["details"]["mnemonic"], anchor.data["details"]["email"], password)


charset = charsets[anchor.data["parameters"]["charset"]]
print("Starting bruteforce with charset[{}]...".format(charset))

password = brute.force(int(anchor.data["depth"]), charset, anchor.data["parameters"]["minimum"], 100, check, cache)
if password:
	print("Password is {}. Found in {} guesses.".format(password[0], password[1]))
	anchor.data["details"]["password"] = password[0]
	anchor.data["success"] = True
	anchor.data["depth"] = int(password[1])
	anchor.save()