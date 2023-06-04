foo = ''
for i in range(3):
	foo += 'a'
	for j in range(3):
		foo += '5'
		for k in range(3):
			foo += '|'

print(foo)