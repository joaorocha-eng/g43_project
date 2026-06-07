from classes.gclass import Gclass
class Agency(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_id','_name','_start_date']
    header = 'Agencies'
    des = ['Id','Name','Start Date']
    def __init__(self, id, name, start_date=None):
        super().__init__()
        id = Agency.get_id(id)
        self._id = id
        self._name = name
        if start_date and isinstance(start_date, str):
            if ' ' in start_date:
                start_date = start_date.split()[0]
            elif 'T' in start_date:
                start_date = start_date.split('T')[0]
        self._start_date = start_date
        Agency.obj[id] = self
        Agency.lst.append(id)
        
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
    def start_date(self):
        return self._start_date
    @start_date.setter
    def start_date(self, start_date):
        if start_date and isinstance(start_date, str):
            if ' ' in start_date:
                start_date = start_date.split()[0]
            elif 'T' in start_date:
                start_date = start_date.split('T')[0]
        self._start_date = start_date
