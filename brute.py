import math
import itertools

def force(start_depth, charset, minimum, maximum, check_callback, cache_callback):
	attempts = 0
	last_depth = start_depth
	for password_length in range(minimum, maximum):
		for guess in itertools.product(charset, repeat=password_length):
			attempts += 1
			if attempts < last_depth:
				continue

			guess = ''.join(guess)
			if check_callback(guess) == 1:
				return (guess, attempts)

			print("- {} - permutations: {}".format(guess, attempts), end="\r")
			if (math.floor(attempts / 1000) * 1000) > last_depth:
				last_depth = attempts
				cache_callback(last_depth)

	return False