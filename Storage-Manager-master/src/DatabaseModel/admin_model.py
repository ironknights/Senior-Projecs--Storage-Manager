"""Query and data actions for business rules and administrative functions

Code written by Jacquesne Jones unless otherwise specified.
"""

from .base_model import BaseModel
from src.DatabaseORM.admin_orm import BusinessRule


class BusinessRuleModel(BaseModel):
    def get_rule(self, rule):
        """Returns a specific rule by string"""
        return self.session.query(BusinessRule).filter(BusinessRule.rule == rule).one()


class RuleExceptionModel(BaseModel):
    pass
