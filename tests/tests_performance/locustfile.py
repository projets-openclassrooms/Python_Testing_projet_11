from locust import HttpUser, task, between
from random import choice

competitions = ["Spring Festival", "Fall Classic"]


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
    def showFormBook(self):
        competition = choice(competitions)
        club = "She Lifts"
        self.client.get(f"/book/{competition}/{club}")

    @task(4)
    def purchase_places(self):
        self.client.post("/purchasePlaces", data={
            "club": "Simply Lift",
            "competition": "Spring Festival",
            "places": "2"
        })

    @task(5)
    def display_dashboard(self):
        self.client.get("/dashboard")

    @task(5)
    def logout(self):
        self.client.get("/logout")

