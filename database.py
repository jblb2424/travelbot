import psycopg2
class Database:
	def __init__(self):
		self.connection = psycopg2.connect(
			database = "detbl8o7irm01l",
			user = 'zliqihqjzalfmn',
			password = "a7b79b4a08b4029d661b9b3134d9fb2c9ae4989fbe7a229ca02232db0738ef39",
			host = 'ec2-54-146-142-58.compute-1.amazonaws.com',
			port = '5432'
		)
		self.cur = self.connection.cursor()

	def close_connection(self):
		self.connection.close()
		self.cur.close()

	#PENDING FOLLOW TABLE - all people we will follow
	def save_pending_follow(self, account, person_name):
		self.cur.execute("INSERT INTO follow_pending (account, person_name) VALUES (%s, %s)", [account, person_name])
		self.connection.commit()	
	
	def delete_pending_follows(self):
		self.cur.execute("DELETE from follow_pending")
		self.connection.commit()

	def find_pending_follows(self):
		self.cur.execute("SELECT distinct(account, person_name) from follow_pending")
		return self.cur.fetchall()


	#FOLLOW TABLE - all people we are currently following
	def save_follower(self, account, follow_time):	
		self.cur.execute("INSERT INTO follow (account, follow_time) VALUES (%s, %s)", (account, follow_time))
		self.connection.commit() # <--- makes sure the change is shown in the database

	def find_stale_following(self, date_followed_offset):
		self.cur.execute("SELECT account from follow where follow_time < (%s)", [date_followed_offset])
		return self.cur.fetchall()

	def delete_stale_following(self, date_followed_offset):
		self.cur.execute("DELETE from follow where follow_time < (%s)", [date_followed_offset])
		self.connection.commit()


	#PHOTOS TABLE - holds ID's of all photos posted
	def save_photo(self, photo_reference):
		self.cur.execute("INSERT INTO photos (photo_reference) VALUES (%s);", [photo_reference])
		self.connection.commit()

	def photo_used(self, photo_reference):
		self.cur.execute("SELECT photo_reference from photos where photo_reference = (%s)", [photo_reference])
		return self.cur.fetchone() is not None

	#####Initial DB table creation####
	def create_table(self):
		self.cur.execute("CREATE TABLE follow (id serial PRIMARY KEY, account varchar, follow_time timestamp);")
		self.connection.commit()
		self.connection.close()
		cur.close()