import math


def factor (num_):
	def check (a_, b_):
		c = num - a_ * b_
		return c > 0 and c <= 127

	num = int (num_)
	a = int (math.sqrt (num)) - 2
	b = a
	while (not check (a, b)):
		if num - a * b > 127:
			a += 1
			a, b = b, a
		if a > num_:
			print 'broken'
			return None

	return [a, b, num - a * b]

