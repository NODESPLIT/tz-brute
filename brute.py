import math
import time
import string
import itertools
import multiprocessing

def permutate(packet, thread, threads, offset, count, check, timestamp):
	amount = 0
	for guess in packet:
		guess = "".join(guess)
		if thread == threads - 1:
			total = offset + (amount * threads)
			percent = round((total/count)*100, 6)
			now = time.time()
			speed = round((amount / (now - timestamp)) * threads)
			print("  - {} - permutations: {} / {} ({}%) - threads: {} - speed: {} p/s".format(guess, total, count, percent, threads, speed), end="      \r")
		if check(guess) == 1:
			return guess
		amount += 1
	return None

def process(result):
	global found
	if result:
		found = result


def force(start, charset, minimum, maximum, chunk, check, cache):
	global found
	found = None

	threads = multiprocessing.cpu_count()
	offset = start[1]

	for length in range(minimum, maximum):
		if length < start[0]:
			continue

		permutations = itertools.product(charset, repeat=length)
		count = len(charset) ** length
		offset = start[1]

		while offset < count:
			pool = multiprocessing.Pool()

			for thread in range(0, threads):
				leap = thread * chunk
				pool.apply_async(permutate, args=(itertools.islice(permutations, offset + leap, offset + leap + chunk), thread, threads, offset, count, check, time.time()), callback=process)
			
			pool.close()
			pool.join()

			if found:
				return found

			offset += threads * chunk
			cache(length, offset)

		offset = 0

	return False