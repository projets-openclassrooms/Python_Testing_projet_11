from utils.settings import *
from flask import Flask, render_template, request, redirect, flash, url_for

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = Load_Competitions()
clubs = load_clubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions)
    except IndexError:
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
def purchase_places():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])

    # ancien calcul
    # competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
    # club['points'] = int(club['points']) - places_required

    # Calcul des places requises  equitablement et sauvegarder resultat
    if competition and club:
        points_required = places_required
        club_points = int(club['points'])
        competition_places = int(competition['numberOfPlaces'])
        if club_points >= points_required:
            competition['numberOfPlaces'] = competition_places - places_required
            club['points'] = club_points - points_required
            print("points_required", points_required)
            print("club['points'] ", club['points'])
            print("competition['numberOfPlaces'] ", competition['numberOfPlaces'])
            flash('Great-booking complete!')
        else:
            flash('Not enough points to complete the booking')
    else:
        flash('Something went wrong-Try again.')

    return render_template('welcome.html', club=club, competitions=competitions), 400


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
