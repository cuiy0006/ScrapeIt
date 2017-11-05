
def consumer():
	r = ''
	print('first consumer execution. 11111111111111111')
	while True:
		n = yield r # receive n from send. But yield value immediately when arriving at the block
		print('After yield')
		if not n:
			return # terminate the generator
		print('[Consumer] consumes %s...' % n)
		r = '200 OK'

def produce(c):
	c.send(None) # make consumer block at n = yield r, when r is ''
	print('first produce execution')
	n = 0
	while n < 5:
		n = n + 1
		print('[Producer] produces %s...' %n)
		r = c.send(n)
		print('[Producer] consumer return: %s' %r)
	c.send(None)

c = consumer()
produce(c)