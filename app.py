import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate

app = Flask(__name__)
moment = Moment(app)
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
	shows = db.relationship('Show', backref = 'venues')

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
	shows = db.relationship('Show', backref = 'artists')

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

#Views

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

@app.route('/')
def index():
  return render_template('pages/home.html')

@app.route('/venues')
def venues():
  data = Venue.query.all()
  area = Venue.query.order_by(Venue.city)
  return render_template('pages/venues.html', areas=area, venue=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term')
  data = []
  venues = db.session.query(Venue).filter(Venue.name.ilike('%search_term%'))
  for venue in venues:
    num_upcoming_shows = 0
    shows = db.session.query(Show).filter(Show.venue_id == venue.id)
    for show in shows:
      if (show.start_time > datetime.now()):
        num_upcoming_shows += 1;
    data.append({"id": venue.id, "name": venue.name, "num_upcoming_shows": num_upcoming_shows})
  response = {"count": venues.count(), "data": data}
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term'))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  data = Venue.query.get(venue_id)
  return render_template('pages/show_venue.html', venue=data)

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm()
  error = False
  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  address = request.form.get('address')
  phone = request.form.get('phone')
  genres = request.form.get('genres')
  facebook_link = request.form.get('facebook_link')
  try:
    venue = Venue(name=name, city = city, state = state,address = address, phone = phone, genres = [genres],facebook_link = facebook_link)
    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Venue ' + request.form.get('name') + ' could not be listed.')
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    flash('Venue ' + request.form.get('name') + ' was successfully listed!')
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    Venue.query.filter_by(id=venue).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return None

@app.route('/artists')
def artists():
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term')
  data = []
  artists = db.session.query(Artist).filter(Artist.name.ilike('%search_term%'))
  for artist in artists:
    num_upcoming_shows = 0
    shows = db.session.query(Show).filter(Show.artist_id == artist.id)
    for show in shows:
      if (show.start_time > datetime.now()):
        num_upcoming_shows += 1;
    data.append({"id": artist.id, "name": artist.name, "num_upcoming_shows": num_upcoming_shows})
  response = {"count": artists.count(), "data": data}
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term'))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  data = Artist.query.get(artist_id)
  return render_template('pages/show_artist.html', artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm()
  error = False
  artist = Artist.query.get(artist_id)
  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  address = request.form.get('address')
  phone = request.form.get('phone')
  genres = request.form.get('genres')
  facebook_link = request.form.get('facebook_link')
  try:
    artist.name = 'name'
    artist.city = 'city'
    artist.state = 'state'
    artist.address = 'address'
    artist.phone = 'phone'
    artist.genres = 'genres'
    artist.facebook_link = 'facebook_link'
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm()
  error = False
  venue = ArtVenueist.query.get(venue_id)
  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  address = request.form.get('address')
  phone = request.form.get('phone')
  genres = request.form.get('genres')
  facebook_link = request.form.get('facebook_link')
  try:
    venue.name = 'name'
    venue.city = 'city'
    venue.state = 'state'
    venue.address = 'address'
    venue.phone = 'phone'
    venue.genres = 'genres'
    venue.facebook_link = 'facebook_link'
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return redirect(url_for('show_venue', venue_id=venue_id))

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm()
  error = False
  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  address = request.form.get('address')
  phone = request.form.get('phone')
  genres = request.form.get('genres')
  facebook_link = request.form.get('facebook_link')
  try:
    artist = Artist(name=name, city = city, state = state,address = address, phone = phone, genres = [genres],facebook_link = facebook_link)
    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Artist ' + request.form.get('name') + ' could not be listed.')
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    flash('Artist ' + request.form.get('name') + ' was successfully listed!')
    return render_template('pages/home.html')

@app.route('/shows')
def shows():
  data = Show.query.all()
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm()
  error = False
  venue_id = request.form.get('venue_id')
  artist_id = request.form.get('artist_id')
  start_time = request.form.get('start_time')
  try:
    show = Show(venue_id = venue_id, artist_id = artist_id, start_time = start_time)
    db.session.add(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    flash('Show was successfully listed!')
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

if __name__ == '__main__':
    app.run()

# Data

venue1 = Venue(
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
    image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    num_past_shows=1,
    num_upcoming_shows=0)

venue2 = Venue(
    name="The Dueling Pianos Bar",
    genres=["Classical", "R&B", "Hip-Hop"],
    address="335 Delancey Street",
    city="New York",
    state="NY",
    phone="914-003-1132",
    website="https://www.theduelingpianos.com",
    facebook_link="https://www.facebook.com/theduelingpianos",
    seeking_talent=False,
    image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    num_past_shows=0,
    num_upcoming_shows=0)

venue3 = Venue(
    name="Park Square Live Music & Coffee",
    genres=["Rock n Roll", "Jazz", "Classical", "Folk"],
    address="34 Whiskey Moore Ave",
    city="San Francisco",
    state="CA",
    phone="415-000-1234",
    website="https://www.parksquarelivemusicandcoffee.com",
    facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    seeking_talent=False,
    image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    num_past_shows=1,
    num_upcoming_shows=1)

artist4 = Artist(
    id=4,
    name="Guns N Petals",
    genres=["Rock n Roll"],
    city="San Francisco",
    state="CA",
    phone="326-123-5000",
    website="https://www.gunsnpetalsband.com",
    facebook_link="https://www.facebook.com/GunsNPetals",
    seeking_venue=True,
    seeking_description="Looking for shows to perform at in the San Francisco Bay Area!",
    image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    num_past_shows=1,
    num_upcoming_shows=0)

artist5 = Artist(
    id=5,
    name="Matt Quevedo",
    genres=["Jazz"],
    city="New York",
    state="NY",
    phone="300-400-5000",
    facebook_link="https://www.facebook.com/mattquevedo923251523",
    seeking_venue=False,
    image_link="https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    num_past_shows=1,
    num_upcoming_shows=0)

artist6 = Artist(
    id=6,
    name="The Wild Sax Band",
    genres=["Jazz", "Classical"],
    city="San Francisco",
    state="CA",
    phone="432-325-5432",
    seeking_venue=False,
    image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    num_past_shows=0,
    num_upcoming_shows=3)

show1 = Show(
    venue_id=1,
    artist_id=4,
    start_time="2019-05-21T21:30:00.000Z")

show2 = Show(
    venue_id=3,
    artist_id=5,
    start_time="2019-06-15T23:00:00.000Z")

show3 = Show(
    venue_id=3,
    artist_id=6,
    start_time="2035-04-01T20:00:00.000Z")

show4 = Show(
    venue_id=3,
    artist_id=6,
    start_time="2035-04-08T20:00:00.000Z")

show5 = Show(
    venue_id=3,
    artist_id=6,
    start_time="2035-04-15T20:00:00.000Z")

# db.session.add_all([venue1, venue2, venue3, artist4, artist5, artist6, show1, show2, show3, show4, show5])
# db.session.commit()
# db.session.close()