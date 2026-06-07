from classes.gclass import Gclass

class AgencyMission(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_id', '_agency', '_mission', '_transaction_date', '_amount']
    header = 'Agency Missions'
    des = ['Id', 'Agency ID', 'Mission ID', 'Transaction Date', 'Amount']

    def __init__(self, agency, mission, transaction_date, amount):
        from classes.agency import Agency
        from classes.mission import Mission
        super().__init__()
        
        self._agency = int(agency) if str(agency).isdigit() else agency
        self._mission = int(mission) if str(mission).isdigit() else mission
        if transaction_date and isinstance(transaction_date, str):
            if ' ' in transaction_date:
                transaction_date = transaction_date.split()[0]
            elif 'T' in transaction_date:
                transaction_date = transaction_date.split('T')[0]
        self._transaction_date = transaction_date
        self._amount = int(amount) if str(amount).isdigit() else amount
        
        synth_id = f"{self._agency}_{self._mission}_{self._transaction_date}"
        self._id = synth_id
        
        AgencyMission.obj[synth_id] = self
        if synth_id not in AgencyMission.lst:
            AgencyMission.lst.append(synth_id)
        
        ag_obj = Agency.obj.get(self._agency)
        ms_obj = Mission.obj.get(self._mission)
        if ag_obj:
            if not hasattr(ag_obj, 'participations'): 
                ag_obj.participations = []
            ag_obj.participations.append(self)
        if ms_obj:
            if not hasattr(ms_obj, 'participations'): 
                ms_obj.participations = []
            ms_obj.participations.append(self)

    def __repr__(self):
        ag_name = self.agency.name if self.agency else str(self._agency)
        ms_name = self.mission.name if self.mission else str(self._mission)
        return (f"AgencyMission({ag_name} <-> {ms_name}, "
                f"{self.transaction_date}, ${self.amount:,.0f})")

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, id):
        self._id = id

    @property
    def agency_id(self):
        return self._agency
    @agency_id.setter
    def agency_id(self, agency_id):
        self._agency = agency_id

    @property
    def mission_id(self):
        return self._mission
    @mission_id.setter
    def mission_id(self, mission_id):
        self._mission = mission_id

    @property
    def agency(self):
        from classes.agency import Agency
        return Agency.obj.get(self._agency)

    @property
    def mission(self):
        from classes.mission import Mission
        return Mission.obj.get(self._mission)

    @property
    def transaction_date(self):
        return self._transaction_date
    @transaction_date.setter
    def transaction_date(self, transaction_date):
        if transaction_date and isinstance(transaction_date, str):
            if ' ' in transaction_date:
                transaction_date = transaction_date.split()[0]
            elif 'T' in transaction_date:
                transaction_date = transaction_date.split('T')[0]
        self._transaction_date = transaction_date

    @property
    def amount(self):
        return self._amount
    @amount.setter
    def amount(self, amount):
        self._amount = amount

    @classmethod
    def remove(cls, p):
        obj = cls.obj[p]
        command = (f'DELETE FROM AgencyMission '
                   f'WHERE agency_id={obj.agency_id} '
                   f'AND mission_id={obj.mission_id} '
                   f'AND transaction_date="{obj.transaction_date}"')
        cls.sqlexe(command)
        cls.lst.remove(p)
        del cls.obj[p]

    @classmethod
    def insert(cls, p):
        obj = cls.obj[p]
        command = (f'INSERT INTO AgencyMission (agency_id, mission_id, transaction_date, amount) '
                   f'VALUES({obj.agency_id}, {obj.mission_id}, "{obj.transaction_date}", {obj.amount})')
        cls.sqlexe(command)

    @classmethod
    def update(cls, p):
        obj = cls.obj[p]
        parts = p.split("_")
        orig_agency = parts[0]
        orig_mission = parts[1]
        orig_date = parts[2]
        
        command = (f'UPDATE AgencyMission SET '
                   f'agency_id={obj.agency_id}, '
                   f'mission_id={obj.mission_id}, '
                   f'transaction_date="{obj.transaction_date}", '
                   f'amount={obj.amount} '
                   f'WHERE agency_id={orig_agency} '
                   f'AND mission_id={orig_mission} '
                   f'AND transaction_date="{orig_date}"')
        cls.sqlexe(command)
        
        new_key = f"{obj.agency_id}_{obj.mission_id}_{obj.transaction_date}"
        if new_key != p:
            obj.id = new_key
            cls.obj[new_key] = obj
            del cls.obj[p]
            idx = cls.lst.index(p)
            cls.lst[idx] = new_key

        
    
        
    