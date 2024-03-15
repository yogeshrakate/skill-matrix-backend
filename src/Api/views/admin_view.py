import asyncio
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import APIRouter, status, Request, Depends

from ..pydantic_models import *
from ..helper import get_db, verify_user
from src.Api.models import (Competency, Designation, Project,
                             Skill, Permission, Role)


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(verify_user)],
    # responses={404: {"description": "Not found"}},
)

class GenericCrudView:
    """
    Generic Class to get the CRUD operation.
    """
    def __init__(self, model, response_model) -> None:
        '''
        Init method.
        '''
        self.model = model
        self.keys = response_model.__annotations__
    
    def get_object(self, db:Session, id):
        """
        Get object method.
        """
        db_obj = db.query(self.model).filter(self.model.id==id).first()
        return db_obj

    def extract_key_value(self, obj):
        data = {}
        attributes = dict(obj.__dict__.items())
        for key in self.keys:
            data[key] = attributes[key]
            data['id'] = attributes['id']
        return data
    
    def get(self, db: Session, id):
        """
        Get method to retrive a single object.
        """
        db_obj = self.get_object(db, id)
        data = self.extract_key_value(db_obj)
        if db_obj:
            data_dict = {
            "message": f"{self.model.__tablename__} Retrived Successful.",
            "data": {
                **data
                }
            }
            return JSONResponse(
                status_code=200,
                content= data_dict
            )
        else:
            data_dict = {
            "message": f"Failed to get {self.model.__tablename__} .",
            "data": {
                **db_obj.__dict__
                }
            }
            return JSONResponse(
                status_code=400,
                content= data_dict
            )
    
    def create(self, db: Session, data_dict: dict):
        """
        Create method to create an object.
        """
        try:
            db_obj = self.model(**data_dict)
            db.add(db_obj)
            db.commit()
            db.close()
        except:
            db_obj =  None
        if db_obj:
            data_dict = {
            "message": f"{self.model.__tablename__} Created Successfully.",
            "data": data_dict
            }
            return JSONResponse(
                    status_code=200,
                    content= data_dict
                    )
        else:
            data_dict = {
            "message": f"Failed to create {self.model.__tablename__} .",
            "data": data_dict
            }
            return JSONResponse(
                status_code=400,
                content= data_dict
            )

    def list_data(self, db: Session, skip: int = 0, limit: int = 10):
        """
        Get the list of objects.
        """
        db_obj_list = db.query(self.model).offset(skip).limit(limit).all()
        data_list = []
        for obj in db_obj_list:
            data = self.extract_key_value(obj)
            data_list.append(data)
        if data_list:
            data_dict = {
            "message": f"{self.model.__tablename__} list retrived Successfully.",
            "data": [*data_list]
            }
            return JSONResponse(
                status_code=200,
                content= data_dict
            )
        else:
            data_dict = {
            "message": f"Failed to retirive {self.model.__tablename__} list.",
            "data": {}
            }
            return JSONResponse(
                status_code=400,
                content= data_dict
            )

    def update(self, db: Session, id, data_dict: dict):
        """
        Update method to update the given fields in the objects.
        """
        db_obj = self.get_object(db, id)
        if db_obj:
            try:
                for key, value in data_dict.items():
                    setattr(db_obj, key, value)
                db.commit()
                # db.refresh(db_obj)
            except:
                db.rollback()
                data_dict = {
                    "message": f"Failed to Update {self.model.__tablename__} .",
                    "data": {}
                    }
                return JSONResponse(
                    status_code=400,
                    content= data_dict
                )
            data = self.extract_key_value(db_obj)
            data_dict = {
            "message": f"{self.model.__tablename__} Updated Successfully.",
            "data": {
                **data
                }
            }
            return JSONResponse(
                status_code=200,
                content= data_dict
            )
        else:
            data_dict = {
            "message": f"Failed to retrive {self.model.__tablename__} .",
            "data": {}
            }
            return JSONResponse(
                status_code=400,
                content= data_dict
            )  

    def delete(self, db: Session, id):
        """
        Delete method to delete an object.
        """
        db_obj = self.get_object(db, id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            db.close()
            data_dict = {
                    "message": f"{self.model.__tablename__} Deleted Successfully.",
                    "data": {}
                    }
            return JSONResponse(
                status_code=200,
                content= data_dict
            )
        else:
            data_dict = {
                    "message": f"Failed to Delete {self.model.__tablename__} .",
                    "data": {}
                    }
            return JSONResponse(
                status_code=400,
                content= data_dict
            )


# Actual Admin views starts here

#Product Crud
project_crud = GenericCrudView(Project, response_model=PydanticProject)

@router.post("/project/create")
def create_project(request: PydanticProject, db: Session = Depends(get_db)):
    '''
    Create Project.
    '''
    data = project_crud.create(db, request.model_dump())
    return data

@router.put("/project/{id}")
def update_project(id, request:PydanticProject, db: Session = Depends(get_db)):
    '''
    Update Project.
    '''
    data = project_crud.update(db, id, request.model_dump())
    return data

@router.get("/project/{id}")
def get_project(id, db: Session = Depends(get_db)):
    '''
    Get Project.
    '''
    data = project_crud.get(db, id)
    return data

@router.get("/project-list")
def get_project_list( db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    '''
    Get Project List.
    '''
    data = project_crud.list_data(db, skip, limit)
    return data

@router.delete("/project/{id}")
def delete_project(id, db: Session = Depends(get_db)):
    '''
    Delete Project.
    '''
    data = project_crud.delete(db, id)
    return data


#Skill Crud
skill_crud = GenericCrudView(Skill, response_model=PydanticSkill)

@router.post("/skill/create")
def create_skill(request: PydanticSkill, db: Session = Depends(get_db)):
    '''
    Create Skill.
    '''
    data = skill_crud.create(db, request.model_dump())
    return data

@router.put("/skill/{id}")
def update_skill(id, request:PydanticSkill, db: Session = Depends(get_db)):
    '''
    Update Skill.
    '''
    data = skill_crud.update(db, id, request.model_dump())
    return data

@router.get("/skill/{id}")
def get_skill(id, db: Session = Depends(get_db)):
    '''
    Get Skill.
    '''
    data = skill_crud.get(db, id)
    return data

@router.get("/skill-list")
def get_skill_list( db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    '''
    Get Skill List.
    '''
    data = skill_crud.list_data(db, skip, limit)
    return data

@router.delete("/skill/{id}")
def delete_skill(id, db: Session = Depends(get_db)):
    '''
    Delete Skill.
    '''
    data = skill_crud.delete(db, id)
    return data


#Designation Crud
designation_crud = GenericCrudView(Designation, response_model=PydanticDesignation)

@router.post("/project/create")
def create_designation(request: PydanticDesignation, db: Session = Depends(get_db)):
    '''
    Create Designation.
    '''
    data = designation_crud.create(db, request.model_dump())
    return data

@router.put("/designation/{id}")
def update_designation(id, request:PydanticDesignation, db: Session = Depends(get_db)):
    '''
    Update Designation.
    '''
    data = designation_crud.update(db, id, request.model_dump())
    return data

@router.get("/designation/{id}")
def get_designation(id, db: Session = Depends(get_db)):
    '''
    Get Designation.
    '''
    data = designation_crud.get(db, id)
    return data

@router.get("/designation-list")
def get_designation_list( db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    '''
    Get Designation List.
    '''
    data = designation_crud.list_data(db, skip, limit)
    return data

@router.delete("/designation/{id}")
def delete_designation(id, db: Session = Depends(get_db)):
    '''
    Delete Designation.
    '''
    data = designation_crud.delete(db, id)
    return data


#Competency Crud
competency_crud = GenericCrudView(Competency, response_model=PydanticCompetency)

@router.post("/competency/create")
def create_competency(request: PydanticCompetency, db: Session = Depends(get_db)):
    '''
    Create Competency.
    '''
    data = competency_crud.create(db, request.model_dump())
    return data

@router.put("/competency/{id}")
def update_competency(id, request:PydanticCompetency, db: Session = Depends(get_db)):
    '''
    Update Competency.
    '''
    data = competency_crud.update(db, id, request.model_dump())
    return data

@router.get("/competency/{id}")
def get_competency(id, db: Session = Depends(get_db)):
    '''
    Get Competency.
    '''
    data = competency_crud.get(db, id)
    return data

@router.get("/competency-list")
def get_competency_list( db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    '''
    Get Competency List.
    '''
    data = competency_crud.list_data(db, skip, limit)
    return data

@router.delete("/competency/{id}")
def delete_competency(id, db: Session = Depends(get_db)):
    '''
    Delete Competency.
    '''
    data = competency_crud.delete(db, id)
    return data


#Permission Crud
permission_crud = GenericCrudView(Permission, response_model=PydanticPermission)

@router.post("/permission/create")
def create_permission(request: PydanticPermission, db: Session = Depends(get_db)):
    '''
    Create Permission.
    '''
    data = permission_crud.create(db, request.model_dump())
    return data

@router.put("/permission/{id}")
def update_permission(id, request:PydanticPermission, db: Session = Depends(get_db)):
    '''
    Update Permission.
    '''
    data = permission_crud.update(db, id, request.model_dump())
    return data

@router.get("/permission/{id}")
def get_permission(id, db: Session = Depends(get_db)):
    '''
    Get Permission.
    '''
    data = permission_crud.get(db, id)
    return data

@router.get("/permission-list")
def get_permission_list( db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    '''
    Get Permission List.
    '''
    data = permission_crud.list_data(db, skip, limit)
    return data

@router.delete("/permission/{id}")
def delete_permission(id, db: Session = Depends(get_db)):
    '''
    Delete Permission.
    '''
    data = permission_crud.delete(db, id)
    return data


#Roles Crud
roles_crud = GenericCrudView(Role, response_model=PydanticRole)

@router.post("/role/create")
def create_role(request: PydanticRole, db: Session = Depends(get_db)):
    '''
    Create Role.
    '''
    data = roles_crud.create(db, request.model_dump())
    return data

@router.put("/role/{id}")
def update_role(id, request:PydanticRole, db: Session = Depends(get_db)):
    '''
    Update Role.
    '''
    data = roles_crud.update(db, id, request.model_dump())
    return data

@router.get("/role/{id}")
def get_role(id, db: Session = Depends(get_db)):
    '''
    Get Role.
    '''
    data = roles_crud.get(db, id)
    return data

@router.get("/role-list")
def get_role_list( db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    '''
    Get Role List.
    '''
    data = roles_crud.list_data(db, skip, limit)
    return data

@router.delete("/role/{id}")
def delete_role(id, db: Session = Depends(get_db)):
    '''
    Delete Role.
    '''
    data = roles_crud.delete(db, id)
    return data
