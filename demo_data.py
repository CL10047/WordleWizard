def demoUsers():
	return [
		('admin@wordlewizard.com', 'password', 2, 'chris'),
		('mark@wordlewizard.com', 'password', 1, 'mark'),
		('johndoe@example.com', 'password', 0, 'johnny'),
		('janedoe@example.com', 'password', 0, 'jane'),
		('bob@example.com', 'password', 0, 'bob')
	]

def demoUserStats():
	return [
		(3, 1, 0),
		(3, 1, 0),
		(3, 2, 0),
		(3, 2, 0),
		(3, 2, 0),
		(3, 3, 0),
		(3, 4, 0),
		(3, 4, 0),
		(3, 5, 0),
		(3, 5, 0),
		(3, 5, 0),
		(3, 6, 0),
		(3, 0, 1),
		(3, 0, 1),
		(3, 0, 1),
        (4, 1, 0),
		(4, 1, 0),
		(4, 1, 0),
		(4, 1, 0),
		(4, 2, 0),
		(4, 4, 0),
		(4, 4, 0),
		(4, 4, 0),
		(4, 5, 0),
		(4, 5, 0),
		(4, 6, 0),
		(4, 6, 0),
		(4, 6, 0),
		(4, 0, 1),
		(4, 0, 1),
        (5, 2, 0),
		(5, 2, 0),
		(5, 2, 0),
		(5, 2, 0),
		(5, 2, 0),
		(5, 3, 0),
		(5, 3, 0),
		(5, 4, 0),
		(5, 6, 0),
		(5, 6, 0),
		(5, 6, 0),
		(5, 6, 0),
		(5, 6, 0),
		(5, 6, 0),
		(5, 0, 1),
    ]

def demoExtraStats():
	return [
		(3, 12, 15, 12/15 * 100, (2*1+3*2+1*3+2*4+3*5+1*6)/12, 2, 3, 1, 2, 3, 1, 3),
		(4, 13, 15, 13/15 * 100, (4*1+1*2+0*3+2*4+2*5+3*6)/13, 4, 1, 0, 2, 2, 3, 2),
		(5, 14, 15, 14/15 * 100, (0*1+5*2+2*3+1*4+0*5+5*6)/13, 0, 5, 2, 1, 0, 6, 1)
	]

def demoFeedbacks():
	return [
		('good website', 'johndoe@example.com'),
		('bad website', ''),
		('good style', 'brianwilson@example.com'),
	]