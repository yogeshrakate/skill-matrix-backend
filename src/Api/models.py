import uuid
import datetime

from typing import List
from typing import Optional
from sqlalchemy import (create_engine, ForeignKey, String,
                         Column, Integer, Boolean, DateTime, func)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from .database import Base

# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship


class BaseAbs(Base):
    __abstract__ = True

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(String, default="New User")
    updated_by = Column(String)
    

class Permission(BaseAbs):
    __tablename__ = "permission"

    name = Column(String)
    operation = Column(String)
    roles = relationship('Role', secondary='role_permission', back_populates='permissions')


class Role(BaseAbs):
    __tablename__ = "role"

    role_name = Column(String, nullable=False)
    permissions = relationship('Permission', secondary='role_permission', back_populates='roles')
    users = relationship('UserProfile', secondary='user_role', back_populates='roles')


class Project(BaseAbs):
    __tablename__ = "project"

    project_name = Column(String, nullable=False)
    users = relationship('UserProfile', secondary='user_project', back_populates='projects')


class RolePermission(Base):
    __tablename__ = 'role_permission'

    role_id = Column(String, ForeignKey('role.id'), primary_key=True)
    permission_id = Column(String, ForeignKey('permission.id'), primary_key=True)
    created_at = Column(DateTime, server_default=func.now())


class UserRole(Base):
    __tablename__ = 'user_role'

    role_id = Column(String, ForeignKey('role.id'), primary_key=True)
    user_profile_id = Column(String, ForeignKey('user_profile.id'), primary_key=True)
    created_at = Column(DateTime, server_default=func.now())

class UserProject(Base):
    __tablename__ = 'user_project'

    project_id = Column(String, ForeignKey('project.id'), primary_key=True)
    user_profile_id = Column(String, ForeignKey('user_profile.id'), primary_key=True)
    created_at = Column(DateTime, server_default=func.now())


class User(BaseAbs):
    __tablename__ = "user"

    full_name = Column(String, nullable=False)
    email_address = Column(String, nullable=False, unique=True)
    user_profile_id = Column(String, ForeignKey('user_profile.id'), unique=True)
    user_profile = relationship('UserProfile', back_populates='user', uselist=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)


class UserProfile(BaseAbs):
    __tablename__ = "user_profile"

    user = relationship('User', back_populates='user_profile', uselist=False)
    manager_id = Column(String, ForeignKey('user_profile.id'))
    team = relationship("UserProfile", foreign_keys=[manager_id], remote_side='UserProfile.id')
    occupied = Column(Boolean, default=False)
    designation_id = Column(String, ForeignKey('designation.id'))
    designation = relationship('Designation', foreign_keys=[designation_id], back_populates='user')
    competency_id = Column(String, ForeignKey('competency.id'))
    competency = relationship('Competency', foreign_keys=[competency_id], back_populates='user_profile')
    roles = relationship('Role', secondary='user_role', back_populates='users')
    projects = relationship('Project', secondary='user_project', back_populates='users')
    emp_skill_mng = relationship('EmpSkill', back_populates='emp_manager', foreign_keys="EmpSkill.emp_manager_id")
    emp_skill_user = relationship('EmpSkill', back_populates='user', foreign_keys="EmpSkill.user_profile_id")
    skill_evaluator = relationship('SkillEvaluator', back_populates='evaluator')


class Skill(BaseAbs):
    __tablename__ = "skill"

    skill_name = Column(String, nullable=False)
    emp = relationship('EmpSkill', back_populates='emp_skill')


class EmpSkill(BaseAbs):
    __tablename__ = "emp_skill"

    user_profile_id = Column(String, ForeignKey('user_profile.id'))
    user = relationship('UserProfile', foreign_keys=[user_profile_id], back_populates='emp_skill_user')
    skill_type = Column(String, nullable=False)
    is_evaluated = Column(Boolean, default=False)
    rate_by_self = Column(Integer)
    emp_manager_id = Column(String, ForeignKey('user_profile.id'))
    emp_manager = relationship('UserProfile', foreign_keys=[emp_manager_id], back_populates='emp_skill_mng')
    certificate = Column(String)
    skill_category = Column(String)
    skill_id = Column(String, ForeignKey('skill.id'))
    emp_skill = relationship('Skill', foreign_keys=[skill_id], back_populates='emp')
    evaluate = relationship('SkillEvaluator', back_populates="employee_skill")


class SkillEvaluator(BaseAbs):
    __tablename__ = "skill_evaluator"

    employee_id = Column(String, ForeignKey('emp_skill.id'), unique=True)
    employee_skill = relationship('EmpSkill', back_populates='evaluate')
    evaluator_id = Column(String, ForeignKey('user_profile.id'))
    evaluator = relationship('UserProfile', back_populates='skill_evaluator')
    evaluator_comment = Column(String)
    evaluator_rating = Column(Integer)


class Designation(BaseAbs):
    __tablename__ = "designation"

    user = relationship('UserProfile', back_populates='designation')
    desg_name = Column(String, nullable=False)


class Competency(BaseAbs):
    __tablename__ = "competency"

    user_profile = relationship('UserProfile', back_populates='competency')
    comp_name = Column(String, nullable=False)

