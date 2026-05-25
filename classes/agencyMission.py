from classes.gclass import Gclass
class AgencyMission(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_agency','Mission','_transaction_date','_amount']
    header = 'AgencyMission'
    des = ['Agency','Mission','transaction date','amount']
    def __init__(self, agency, mission, transaction_date, amount):
        from classes.Agency import Agency
        from classes.Mission import Mission
        super().__init__()
        self._agency = agency
        self._mission = mission
        self._transaction_date = transaction_date
        self._amount = amount
        ag_id = int(agency) if str(agency).isdigit() else agency
        ms_id = int(mission) if str(mission).isdigit() else mission
        ag_obj = Agency.obj.get(ag_id)
        ms_obj = Mission.obj.get(ms_id)
        if ag_obj:
            if not hasattr(ag_obj, 'participations'): ag_obj.participations = []
            ag_obj.participations.append(self)
        if ms_obj:
            if not hasattr(ms_obj, 'participations'): ms_obj.participations = []
            ms_obj.participations.append(self)
        
        # We don't have id so we might just add self to obj list if we had an id.
        # But this doesn't have an id attribute in att.
    def __repr__(self):
        return (f"AgencyMission({self.agency.name} <-> {self.mission.name}, "
                f"{self.transaction_date}, ${self.amount:,.0f})")
    @property
    def agency(self):
        return self._agency
    @agency.setter
    def agency(self, agency):
        self._agency = agency
   
    @property
    def mission(self):
        return self._mission
    @mission.setter
    def mission(self, mission):
        self._name = mission
        
    
        
    