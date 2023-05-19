"""Code written by Deeptanshu Das unless otherwise specified."""

from .base_model import BaseModel
from src.DatabaseORM.sitemap_orm import MapUnit
from src.DatabaseORM.sitemap_orm import MapLine


class MapModel(BaseModel):
    """Base class for Maps"""

    def get_all_lines(self):
        """Function that gets all of the lines"""
        return self.session.query(MapLine)

    def get_all_units(self):
        """Function gets all of the units"""
        return self.session.query(MapUnit)





