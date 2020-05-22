from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Models 

class Venue(db.Model):
	__tablename__ = 'venues'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	genres = db.Column(db.String())
	city = db.Column(db.String(120))
	state = db.Column(db.String(120))
	address = db.Column(db.String(120))
	phone = db.Column(db.String(120))
	website = db.Column(db.String(500))
	facebook_link = db.Column(db.String(500))
	seeking_talent = db.Column(db.Boolean, default=False)
	seeking_description = db.Column(db.Text())
	image_link = db.Column(db.String(500))
	num_past_shows = db.Column(db.Integer())
	num_upcoming_shows = db.Column(db.Integer())
	shows = db.relationship('Show', backref = 'venues', lazy=True)

	def __repr__(self):
		return f'<Venue {self.id}>'

class Artist(db.Model):
	__tablename__ = 'artists'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	genres = db.Column(db.String())
	city = db.Column(db.String(120))
	state = db.Column(db.String(120))
	address = db.Column(db.String(120))
	phone = db.Column(db.String(120))
	website = db.Column(db.String(500))
	facebook_link = db.Column(db.String(500))
	seeking_venue = db.Column(db.Boolean, default=False)
	seeking_description = db.Column(db.Text())
	image_link = db.Column(db.String(500))
	num_past_shows = db.Column(db.Integer())
	num_upcoming_shows = db.Column(db.Integer())
	shows = db.relationship('Show', backref = 'artists', lazy=True)

	def __repr__(self):
		return f'<Artist {self.id}>'

class Show(db.Model):
	__tablename__ = 'shows'

	id = db.Column(db.Integer, primary_key=True)
	venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
	artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
	start_time = db.Column(db.String())

	def __repr__(self):
		return f'<Show {self.id}>'

# Seed Examples

venue = Venue(
  id=1,
  name="The Musical Hop",
  genres=["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  city="San Francisco",
  state="CA",
  address="1015 Folsom Street",
  phone="123-123-1234",
  website="https://www.themusicalhop.com",
  facebook_link="https://www.facebook.com/TheMusicalHop",
  seeking_talent=True,
  seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us.",
  image_link="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/socialmedia/apple/237/rabbit_1f407.png",
  num_past_shows=1,
  num_upcoming_shows=0)

artist = Artist(
  id=1,
  name="Hello World",
  genres=["Rock n Roll"],
  city="San Francisco",
  state="CA",
  phone="326-123-5000",
  website="https://www.helloworld.com",
  facebook_link="https://www.facebook.com/helloworld",
  seeking_venue=True,
  seeking_description="Looking for shows to perform at in the San Francisco Bay Area!",
  image_link="https://i.ytimg.com/vi/7U7Eu8u_tBw/maxresdefault.jpg",
  num_past_shows=1,
  num_upcoming_shows=0)

show = Show(
  venue_id=1,  
  artist_id=1,
  start_time="2019-05-21T21:30:00.000Z")

def clear_data(session):
  meta = db.metadata
  for table in reversed(meta.sorted_tables):
      print('Clear table %s' % table)
      session.execute(table.delete())
  session.commit()

clear_data(db.session)
db.session.add_all([venue, artist, show])
db.session.commit()
db.session.close()