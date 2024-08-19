import json

MAX_PLACES_PER_COMPETITION = 12

def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


# def save_clubs(clubs):
#     with open('clubs.json', 'w') as c:
#         clubs_dict = {"clubs": clubs}
#         json.dump(clubs_dict, c, indent=4)


def Load_Competitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions
