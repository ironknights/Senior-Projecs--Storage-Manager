"""Code written by Jacquesne Jones unless otherwise specified."""

from .base_model import BaseModel
from src.DatabaseORM.tenant_orm import Tenant
from src.DatabaseORM.unit_orm import Unit


class TenantModel(BaseModel):

    def get_list(self):
        return self.session.query(Tenant).order_by(Tenant.last)

    def get_by_ssn(self, ssn):
        """Returns a tenant with a specific social security number"""
        tenant = self.session.query(Tenant).filter(Tenant.ssn == ssn)
        if tenant.count() == 0:
            return None
        else:
            return tenant

    def get_by_unit(self, unit_id):
        tenant = self.session.query(Unit).filter(
            Tenant.unit_id == unit_id)
        return tenant
