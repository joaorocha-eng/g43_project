from flask import render_template, request, session, flash
from classes.agency import Agency
from classes.mission import Mission
from classes.astronaut import Astronaut
from classes.agencyMission import AgencyMission
import subs.analysis_subs as analysisSubs

def get_class_by_name(name):
    if name == "Agency":
        return Agency
    elif name == "Mission":
        return Mission
    elif name == "Astronaut":
        return Astronaut
    elif name == "AgencyMission":
        return AgencyMission
    return Agency

def index(db_path):
    can_edit = (session.get("user") == "root")
 
    entity = request.args.get("entity", session.get("entity", "Agency"))
    session["entity"] = entity
    

    if entity == "Analysis":
        charts = analysisSubs.generate_charts(db_path)
        stats = analysisSubs.get_key_stats(db_path)
        return render_template(
            "index.html",
            entity=entity,
            charts=charts,
            stats=stats,
            butshow="disabled",
            butedit="disabled",
            fields={},
            records=[],
            total_found=0,
            total_total=0,
            search_query="",
            agencies=[],
            missions=[],
            current_id=None,
            can_edit=can_edit
        )

    cls = get_class_by_name(entity)
    
    butshow = "enabled"
    butedit = "disabled"
    
    option = request.args.get("option")
    prev_option = session.get("prev_option", "")
    
    if not can_edit:
        if option not in ["first", "previous", "next", "last", "select"]:
            option = None
        prev_option = ""
    
    if option == "edit":
        butshow, butedit = "disabled", "enabled"
    elif option == "insert":
        butshow, butedit = "disabled", "enabled"
    elif option == "cancel":
        pass
    elif option == "delete":
        obj = cls.current()
        if obj:
            try:
                cls.remove(obj.id)
                flash("Record successfully deleted.", "success")
            except Exception as e:
                flash(f"Error deleting record: {e}", "error")
            if not cls.previous():
                cls.first()
    elif prev_option == "insert" and option == "save":
        try:
            if entity == "Agency":
                id = Agency.get_id(0)
                name = request.form["name"]
                start_date = request.form["start_date"]
                obj = Agency(id, name, start_date)
                Agency.insert(obj.id)
                Agency.last()
                flash("Agency successfully created.", "success")
            elif entity == "Mission":
                id = Mission.get_id(0)
                name = request.form["name"]
                mission_type = request.form["mission_type"]
                obj = Mission(id, name, mission_type)
                Mission.insert(obj.id)
                Mission.last()
                flash("Mission successfully created.", "success")
            elif entity == "Astronaut":
                id = Astronaut.get_id(0)
                name = request.form["name"]
                agency_id = int(request.form["agency_id"])
                obj = Astronaut(id, name, agency_id)
                Astronaut.insert(obj.id)
                Astronaut.last()
                flash("Astronaut successfully created.", "success")
            elif entity == "AgencyMission":
                agency_id = int(request.form["agency_id"])
                mission_id = int(request.form["mission_id"])
                transaction_date = request.form["transaction_date"]
                amount = int(request.form["amount"])
                synth_id = f"{agency_id}_{mission_id}_{transaction_date}"
                
                if synth_id in AgencyMission.obj:
                    flash("This participation record already exists!", "error")
                else:
                    obj = AgencyMission(agency_id, mission_id, transaction_date, amount)
                    AgencyMission.insert(obj.id)
                    AgencyMission.last()
                    flash("Agency Mission participation successfully created.", "success")
        except Exception as e:
            flash(f"Error saving record: {e}", "error")
            
    elif prev_option == "edit" and option == "save":
        try:
            obj = cls.current()
            if obj:
                if entity == "Agency":
                    obj.name = request.form["name"]
                    obj.start_date = request.form["start_date"]
                    Agency.update(obj.id)
                    flash("Agency successfully updated.", "success")
                elif entity == "Mission":
                    obj.name = request.form["name"]
                    obj.mission_type = request.form["mission_type"]
                    Mission.update(obj.id)
                    flash("Mission successfully updated.", "success")
                elif entity == "Astronaut":
                    obj.name = request.form["name"]
                    obj.agency_id = int(request.form["agency_id"])
                    Astronaut.update(obj.id)
                    flash("Astronaut successfully updated.", "success")
                elif entity == "AgencyMission":
                    obj.agency_id = int(request.form["agency_id"])
                    obj.mission_id = int(request.form["mission_id"])
                    obj.transaction_date = request.form["transaction_date"]
                    obj.amount = int(request.form["amount"])
                    AgencyMission.update(obj.id)  
                    flash("Agency Mission participation successfully updated.", "success")
        except Exception as e:
            flash(f"Error updating record: {e}", "error")
            
    elif option == "first":
        cls.first()
    elif option == "previous":
        cls.previous()
    elif option == "next":
        cls.nextrec()
    elif option == "last":
        cls.last()
    elif option == "select" and request.args.get("id"):
        sel_id = request.args.get("id")
        if entity == "Astronaut":
            try: sel_id = float(sel_id)
            except: pass
        elif entity == "Agency" or entity == "Mission":
            try: sel_id = int(sel_id)
            except: pass
        cls.current(sel_id)

    if option in ["insert", "edit"]:
        session["prev_option"] = option
        butshow, butedit = "disabled", "enabled"
    else:
        session["prev_option"] = ""
        butshow, butedit = "enabled", "disabled"

    obj = cls.current()
    if not obj and len(cls.lst) > 0 and option != "insert":
        cls.first()
        obj = cls.current()
        
    fields = {}
    if option == "insert" or len(cls.lst) == 0:
        if entity == "Agency":
            fields = {"id": 0, "name": "", "start_date": ""}
        elif entity == "Mission":
            fields = {"id": 0, "name": "", "mission_type": ""}
        elif entity == "Astronaut":
            fields = {"id": 0, "name": "", "agency_id": ""}
        elif entity == "AgencyMission":
            fields = {"id": "", "agency_id": "", "mission_id": "", "transaction_date": "", "amount": ""}
    else:
        if obj:
            if entity == "Agency":
                fields = {"id": obj.id, "name": obj.name, "start_date": obj.start_date}
            elif entity == "Mission":
                fields = {"id": obj.id, "name": obj.name, "mission_type": obj.mission_type}
            elif entity == "Astronaut":
                fields = {"id": obj.id, "name": obj.name, "agency_id": obj.agency_id}
            elif entity == "AgencyMission":
                fields = {"id": obj.id, "agency_id": obj.agency_id, "mission_id": obj.mission_id, "transaction_date": obj.transaction_date, "amount": obj.amount}

    search_query = request.args.get("search", "").strip().lower()
    
    all_records = []
    for key in cls.lst:
        record_obj = cls.obj.get(key)
        if not record_obj: continue
        
        if entity == "Agency":
            label = f"{record_obj.name} (ID: {record_obj.id})"
            match = not search_query or search_query in record_obj.name.lower() or search_query in str(record_obj.id)
        elif entity == "Mission":
            label = f"{record_obj.name} (ID: {record_obj.id})"
            match = not search_query or search_query in record_obj.name.lower() or search_query in str(record_obj.id) or search_query in record_obj.mission_type.lower()
        elif entity == "Astronaut":
            agency_name = record_obj.agency.name if record_obj.agency else str(record_obj.agency_id)
            label = f"{record_obj.name} (ID: {record_obj.id})"
            match = not search_query or search_query in record_obj.name.lower() or search_query in str(record_obj.id) or search_query in agency_name.lower()
        elif entity == "AgencyMission":
            ag_name = record_obj.agency.name if record_obj.agency else str(record_obj.agency_id)
            ms_name = record_obj.mission.name if record_obj.mission else str(record_obj.mission_id)
            label = f"{ag_name} <-> {ms_name}"
            match = not search_query or search_query in ag_name.lower() or search_query in ms_name.lower() or search_query in str(record_obj.transaction_date)
            
        if match:
            all_records.append({
                "id": key,
                "label": label
            })
            
    total_found = len(all_records)
    all_records = all_records[:100]  

    agencies_list = [{"id": Agency.obj[k].id, "name": Agency.obj[k].name} for k in Agency.lst]
    agencies_list.sort(key=lambda x: x["name"])
    
    missions_list = [{"id": Mission.obj[k].id, "name": Mission.obj[k].name} for k in Mission.lst]
    missions_list.sort(key=lambda x: x["name"])

    return render_template(
        "index.html",
        entity=entity,
        butshow=butshow,
        butedit=butedit,
        fields=fields,
        records=all_records,
        total_found=total_found,
        total_total=len(cls.lst),
        search_query=search_query,
        agencies=agencies_list,
        missions=missions_list,
        current_id=obj.id if obj else None,
        can_edit=can_edit
    )
