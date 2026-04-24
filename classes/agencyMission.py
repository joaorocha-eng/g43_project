class AgencyMission:
    def __init__(self, agency, mission, transaction_date, amount):
        self.agency = agency
        self.mission = mission
        self.transaction_date = transaction_date
        self.amount = amount
        agency.participations.append(self)
        mission.participations.append(self)

    def __repr__(self):
        return (f"AgencyMission({self.agency.name} <-> {self.mission.name}, "
                f"{self.transaction_date}, ${self.amount:,.0f})")
