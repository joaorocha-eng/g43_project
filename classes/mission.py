class Mission:
    def __init__(self, id, name, mission_type, start_date):
        self.id = id
        self.name = name
        self.mission_type = mission_type
        self.start_date = start_date
        self.participations = []

    def __repr__(self):
        return f"Mission({self.name})"
