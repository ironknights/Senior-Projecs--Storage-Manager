"""Code written by Jacquesne Jones unless otherwise specified."""

from .base_model import BaseModel
from src.DatabaseORM.user_orm import User, Permission


class UserModel(BaseModel):

    def get_permission_id(self, title):
        """Gets the id of a permission by the name of the permission"""
        return self.session.query(Permission).filter(Permission.title == title).one().id

    def get_by_name(self, name):
        """Gets the user based on the user name"""
        return self.session.query(User).filter(User.user_id == name).one()
