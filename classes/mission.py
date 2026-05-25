from classes.gclass import Gclass

class Mission(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_id','_name','_mission_type','_start_date']
    header = 'Missions'
    des = ['Id','Name','Mission Type','Start Date']
    def __init__(self, id, name, mission_type, start_date):
        super().__init__()
        id = Mission.get_id(id)
        self._id = id
        self._name = name
        self._mission_type = mission_type
        self._start_date = start_date
        self._participations = []
        Mission.obj[id] = self
        Mission.lst.append(id)

    def __repr__(self):
        return f"Mission({self.name})"
    
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, id):
        self._id = id 
   
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name
        
    @property
    def mission_type(self):
        return self._mission_type
    @mission_type.setter
    def mission_type(self, mission_type):
        self._mission_type = mission_type
   
    @property
    def start_date(self):
        return self._start_date
    @start_date.setter
    def start_date(self, start_date):
        self._start_date = start_date
        
    