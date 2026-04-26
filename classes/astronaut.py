from classes.gclass import Gclass
from classes.Agency import Agency

class Astronaut(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_id','_name','_agency_id']
    header = 'Astronaut'
    des = ['Id','Name','Agency']
    def __init__(self, id, name, agency_id):
        super().__init__()
        id = Astronaut.get_id(id)
        self._id = id
        self._name = name
        self._agency_id = int(agency_id) if str(agency_id).isdigit() else agency_id
        Astronaut.obj[id] = self
        Astronaut.lst.append(id)

    def __repr__(self):
        agency_name = self.agency.name if self.agency else str(self._agency_id)
        return f"Astronaut({self.name}, {agency_name})"
    
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
    def agency_id(self):
        return self._agency_id
    @agency_id.setter
    def agency_id(self, agency_id):
        self._agency_id = agency_id

    @property
    def agency(self):
        return Agency.obj.get(self._agency_id)