from utils.settings import *
from flask import Flask, render_template, request, redirect, flash, url_for, session

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = Load_Competitions()
clubs = load_clubs()
places_to_purchase = {}


def search_club(club_email):
    foundclubs = [club for club in clubs if club['email'] == club_email]
    if len(foundclubs) > 0:
        return foundclubs[0]
    return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    club = search_club(request.form['email'])
    if club:
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash('Sorry, that email was not found')
        return render_template('index.html')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]
    if found_club and found_competition:
        # flash("Here is the form to complete")
        return render_template('booking.html', club=found_club, competition=found_competition), 200
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions), 400


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)
    places_required = request.form['places']

    if not places_required:
        flash("Please enter the number of places to reserve.")
        return render_template('booking.html', club=club, competition=competition), 400

    places_required = int(places_required)
    if not places_required:
        flash("Please enter a valid number.")
        return render_template('booking.html', club=club, competition=competition), 400

    if places_required <= 0:
        flash("You can't book a negative number of places.")
        return render_template('booking.html', club=club, competition=competition)

    if places_required > MAX_PLACES_PER_COMPETITION:
        flash("You can't book more than 12 places in a competition.")
        return render_template('booking.html', club=club, competition=competition)

    places_available = int(competition['numberOfPlaces'])
    club_points = int(club['points'])

 # Checks if required places exceed available points and displays flash message accordingly.
    if places_required > places_available or places_required > club_points:
        flash("You don't have enough points.")
        return render_template('booking.html', club=club, competition=competition)

    total_booked = places_to_purchase.get(competition['name'], 0)
    if total_booked >= MAX_PLACES_PER_COMPETITION:
        flash("You have already booked 12 places for this competition.")
        return render_template('booking.html', club=club, competition=competition)

    if total_booked + places_required > 12:
        flash("You can't book more than 12 places for this competition.")
        return render_template('booking.html', club=club, competition=competition)

    competition['numberOfPlaces'] = str(places_available - places_required)
    club['points'] = str(club_points - places_required)
    places_to_purchase[competition['name']] = total_booked + places_required

    flash("Great-booking complete!")
    return render_template('booking.html', club=club, competition=competition)


# TODO: Add route for points display
@app.route('/dashboard')
def display_dashboard():

    club_email = session.get("club_email")
    if club_email:
        club = [club for club in clubs if club["email"] == club_email][0]
    else:
        club = None
    return render_template('dashboard.html', clubs=clubs, current_club=club)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
