"""Code written by Jacquesne Jones unless otherwise specified."""

from sqlalchemy import Numeric, cast, and_, or_, func
from .base_model import BaseModel
from src.DatabaseORM.unit_orm import Unit, UnitRule, UnitCategory


class UnitModel(BaseModel):
    """Model for unit operations."""
    def get_by_name(self, name):
        """Gets a unit by the identifier of that unit."""
        return self.session.query(Unit).filter(Unit.identifier == name).one()

    def get_sizes(self):
        """Creates a dictionary of all unit sizes for use in drop lists"""
        size_query = self.session.query(UnitRule).join(UnitCategory, UnitRule.category).\
            order_by(UnitCategory.category).\
            order_by(cast(UnitRule.width, Numeric)).order_by(cast(UnitRule.length, Numeric))
        sizes = {}
        for size in size_query:
            sizes[size.size_string] = size.id
        return sizes

    def list_sizes(self):
        """Gets a Python list of all unit sizes for use in drop-down lists and other UI elements."""
        return list(self.get_sizes().keys())

    def get_list(self):
        """Gets all units in order set by user.

        The order element allows for arbitrary ordering of units. By default new units are ordered based on when
        they are created, but this can be changed later.
        """
        return self.session.query(Unit).order_by(Unit.order)

    def get_category_id(self, category):
        """Gets the id of a category by name."""
        return self.session.query(UnitCategory).filter(UnitCategory.category == category).one().id

    def get_link_list(self, unit):
        """Gets a list of all units linked to the given unit

        :return A list of string identifiers for linked units"""
        # First check if already linked, if not, return just empty list
        if not unit.link_group:
            return []
        else:
            # Query for all linked elements
            group = self.session.query(Unit).filter(Unit.link_group == unit.link_group)
            link_list = []
            for item in group:
                link_list.append(item.identifier)
            return link_list

    def get_unlinked_list(self, unit):
        """Gets all units that are NOT linked to the given unit

        :return A list of string identifiers for unlinked units"""
        link_list = []
        # If no link group, get everything except self, otherwise filter out current link
        if not unit.link_group:
            available = self.session.query(Unit).filter(Unit.id != unit.id)
        else:
            # Note...filter only checks for NULL condition with equality, using 'not Unit.link_group' won't work
            available = self.session.query(Unit).filter(
                and_(or_(Unit.link_group != unit.link_group, Unit.link_group == None), Unit.id != unit.id))
        for item in available:
            link_list.append(item.identifier)
        return link_list

    def next_link_group(self):
        """Finds the next link group"""
        max_group = self.session.query(func.max(Unit.link_group)).first()[0]
        # Add 1 if a number was returned
        if max_group:
            max_group += 1
        else:
            max_group = 1
        return max_group

    def update_links(self, add_links, remove_links):
        """Takes two lists of link identifiers to add and remove from link groups"""
        # First remove all units from link group that need to be removed
        if remove_links:
            print(f"Removing: {remove_links}")
            for link in remove_links:
                self.get_by_name(link).link_group = None
        if add_links:
            print(f"Adding: {add_links}")
            # Find current groupings of selected units
            groups = []
            for link in add_links:
                link_group = self.get_by_name(link).link_group
                if link_group not in groups and link_group is not None:
                    groups.append(link_group)
            # If no groups currently assigned to any units, assign them to the next available group
            print(f"Groups: {groups}")
            if not groups:
                group = self.next_link_group()
                print(f"Available: {group}")
            else:
                group = min(groups)     # Set all to the lowest group number
            # Set all to new group
            for link in add_links:
                print(f"Setting {link} to group {group}")
                self.get_by_name(link).link_group = group
        if add_links or remove_links:
            self.session.commit()

    def move_in(self, unit, tenant):
        """Moves a new tenant into a unit"""
        unit.tenant = tenant
        self.database.TransactionModel.add_rent_charge(unit, unit.size.price)
