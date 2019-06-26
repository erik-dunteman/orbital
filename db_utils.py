import sqlite3

'''
NOTES ON SCHEMA:

There is one table, "log", which has fields:
episode, v_x, v_y, radius, wall_dist, mass, fuel, reward

'''

def write(episode, observation, reward):
	#Connect to database
	connection = sqlite3.connect("warehouse.db")
	cursor = connection.cursor()

	add_start = "INSERT INTO log VALUES("
	field0 = str(episode)+", "
	field1 = str(observation[0])+", "
	field2 = str(observation[1])+", "
	field3 = str(observation[2])+", "
	field4 = str(observation[3])+", "
	field5 = str(observation[4])+", "
	field6 = str(observation[5])+", "
	field7 = str(reward)
	add_end = ");"


	add_command = add_start+field0+field1+field2+field3+field4+field5+field6+field7+add_end

	# print(add_command)

	try:
		cursor.execute(add_command)
		# print("Successful Insertion")
	except:
		#that database does not exist
		# print("Database Doesn't Yet Exist")
		build_command = """CREATE TABLE log (
		episode INT,
		v_x FLOAT(8),
		v_y FLOAT(8),
		radius FLOAT(8),
		wall_dist INT,
		mass FLOAT(4),
		fuel INT,
		reward INT)
		"""
		# print(build_command)
		cursor.execute(build_command)
		cursor.execute(add_command)

	connection.commit()
	connection.close()

def fetch_all():
	connection = sqlite3.connect("warehouse.db")
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM log")
	data = cursor.fetchall()
	return data