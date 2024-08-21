from locust import HttpUser, task, between
from random import choice

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.club_emails = [
            "john@simplylift.co",
            "admin@irontemple.com",
            "kate@shelifts.co.uk"
        ]

    @task(1)
    def index_page(self):
        self.client.get("/")

    @task(2)
    def show_summary(self):
        email = choice(self.club_emails)
        self.client.post("/showSummary", data={"email": email})

    @task(3)
    def book_competition(self):
        email = choice(self.club_emails)
        response = self.client.post("/showSummary", data={"email": email})
        if "Welcome" in response.text:
            club_name = response.text.split("Welcome, ")[1].split("!")[0]
            competitions = ["Spring Festival", "Fall Classic"]
            competition = choice(competitions)
            self.client.get(f"/book/{competition}/{club_name}")

    @task(4)
    def purchase_places(self):
        email = choice(self.club_emails)
        response = self.client.post("/showSummary", data={"email": email})
        if "Welcome" in response.text:
            club_name = response.text.split("Welcome, ")[1].split("!")[0]
            competitions = ["Spring Festival", "Fall Classic"]
            competition = choice(competitions)
            places = choice(range(1, 13))
            self.client.post("/purchasePlaces", data={
                "competition": competition,
                "club": club_name,
                "places": places
            })

    @task(1)
    def display_dashboard(self):
        self.client.get("/dashboard")

    @task(1)
    def logout(self):
        self.client.get("/logout")