from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task(1)
    def index(self):
        self.client.get("/")

    @task(2)
    def show_summary(self):
        self.client.post("/showSummary", data={"email": "test@example.com"})

    @task(3)
    def book(self):
        self.client.get("/book/CompetitionName/ClubName")

    @task(4)
    def purchase_places(self):
        self.client.post("/purchasePlaces", data={
            "competition": "CompetitionName",
            "club": "ClubName",
            "places": "2"
        })

    @task(5)
    def dashboard(self):
        self.client.get("/dashboard")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # Attendre entre 1 et 5 secondes entre les tâches
