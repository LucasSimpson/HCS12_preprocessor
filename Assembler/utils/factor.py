import math


def factor (num_, max_):
	def check (a_, b_):
		c = num - a_ * b_
		return c > 0 and c <= max_

	num = int (num_)
	a = int (math.sqrt (num)) - 2
	b = a
	while (not check (a, b)):
		if num - a * b > max_:
			a += 1
			a, b = b, a

	return [a, b, num - a * b]

def long_delay_factor (delay_):
        delay = int (delay_)
        a = int (delay / 50)
        b = 50
        c = delay - (a * b)
        return [a, b, c]

