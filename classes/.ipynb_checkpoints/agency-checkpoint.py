class Agency:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.astronauts = []
        self.participations = []

    def add_astronaut(self, astronaut):
        self.astronauts.append(astronaut)

    def __repr__(self):
        return f"Agency({self.name})"
