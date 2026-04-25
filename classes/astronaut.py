class Astronaut:
    def __init__(self, id, name, agency):
        self.id = id
        self.name = name
        self.agency = agency

    def __repr__(self):
        return f"Astronaut({self.name}, {self.agency.name})"
