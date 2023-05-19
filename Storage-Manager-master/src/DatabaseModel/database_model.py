"""Code written by Jacquesne Jones unless otherwise specified."""

import os
import sys
from sqlalchemy import create_engine, func
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import sessionmaker
from src.Encryption.crypto import Access
from src.DatabaseORM.base_orm import Base
from src.DatabaseORM.tenant_orm import Tenant
from src.DatabaseORM.unit_orm import Unit, UnitCategory, UnitRule
from src.DatabaseORM.user_orm import User, Permission
from src.DatabaseORM.transaction_orm import Transaction, TransactionCategory, Inventory
from src.DatabaseORM.reporting_orm import Report, Form
from src.DatabaseORM.history_orm import UnitHistory, TenantHistory, HistoryCategory
from src.DatabaseORM.admin_orm import BusinessRule, RuleException
from src.DatabaseORM.sitemap_orm import MapUnit
from .admin_model import BusinessRuleModel, RuleExceptionModel
from .history_model import UnitHistoryModel, TenantHistoryModel
from .reporting_model import ReportModel, FormModel
from .sitemap_model import MapModel
from .tenant_model import TenantModel
from .transaction_model import TransactionModel, InventoryModel
from .unit_model import UnitModel
from .user_model import UserModel

# This flags whether or not to show debug information when accessing the database
DEBUG_ECHO = False


class Database:
    """This is the core database model and is where all other data models are accessed.

    This class is what opens and initializes sqlite3 databases for use in the program and ORM.
    It creates and has access to all other data models. A Database object is loaded at runtime and is a
    singleton accessed by all other data models.
    """
    def __init__(self, filename=None):
        self.session = None
        # DatabaseORM
        self.engine = None
        self.filename = filename
        # Query classes
        self.TenantModel = None
        self.UnitModel = None
        self.UserModel = None
        self.TransactionModel = None
        self.InventoryModel = None
        self.ReportModel = None
        self.FormModel = None
        self.UnitHistoryModel = None
        self.TenantHistoryModel = None
        self.BusinessRuleModel = None
        self.RuleExceptionModel = None
        self.MapModel = None
        # If passed a filename go ahead and load at initialization, otherwise leave as None
        if filename:
            self.load(filename)

    def load(self, filename):
        """Loads a sqlite3 database file"""
        if not self.filename:
            self.filename = filename
        try:
            if sys.platform.startswith('win32'):    # Only replace on Windows
                filename = filename.replace("/", "\\\\")    # Needs two backslashes for path on Windows
            path = f'sqlite:///{filename}'
            self.engine = create_engine(path, echo=DEBUG_ECHO)
        except FileNotFoundError as e:
            print(e)
            return False
        # Establish table if needed
        Base.metadata.create_all(self.engine)
        # Create session
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        # Create query objects
        self.TenantModel = TenantModel(self, Tenant)
        self.UnitModel = UnitModel(self, Unit)
        self.UserModel = UserModel(self, User)
        self.TransactionModel = TransactionModel(self, Transaction)
        self.InventoryModel = InventoryModel(self, Inventory)
        self.ReportModel = ReportModel(self, Report)
        self.FormModel = FormModel(self, Form)
        self.UnitHistoryModel = UnitHistoryModel(self, UnitHistory)
        self.TenantHistoryModel = TenantHistoryModel(self, TenantHistory)
        self.BusinessRuleModel = BusinessRuleModel(self, BusinessRule)
        self.RuleExceptionModel = RuleExceptionModel(self, RuleException)
        self.MapModel = MapModel(self, MapUnit)
        # Initialize defaults if necessary
        self.__initialize()

    def __initialize(self):
        """Initializes a brand new database with default settings.

        The core method for initialization is to check if a table that would normally have default data is
        empty, and if so, add the template. On a brand new database this will be all tables and the code will
        initialize everything.

        The reason this is table-specific and runs every time at startup is to allow setting specific tables
        to default without affecting changes elsewhere. For example, the user could reset all permissions
        and the program can simply delete all permissions then run this function again, restoring it to the default
        state.
        """
        # Create default permissions
        if self.session.query(Permission).count() == 0:
            self.session.add(Permission(
                title="Admin",
                create_template=1,
                ssn_reports=1,
                edit_rules=1,
                edit_forms=1,
                edit_reports=1,
                edit_inventory=1,
                edit_exceptions=1,
                manual_exceptions=1,
                allow_incomplete=1
            ))
        # Create default user
        if self.session.query(User).count() == 0:
            self.session.add(User(
                user_id="admin",
                pw_hash=Access.generate_hash("password"),
                permission_id=self.UserModel.get_permission_id("Admin"),
                default_tab="Operations"
            ))
        # -------------------------------------------------------------------------------------
        # Code written by Cameron Howard
        # Create default reports
        if self.session.query(Report).count() == 0:
            self.session.add_all([
                Report(
                    title='Daily',
                    category='Main',
                    description='Daily Menu',
                    filter_string='',
                    filter_values='',
                    contains_ssn=False
                ),
                Report(
                    title='Owner Report',
                    category='Daily',
                    description='Report of the unit rules.',
                    filter_string='select id, category_id, length, width, floor, price from unitrules',
                    filter_values='unitrules;id;category_id;length;width;floor;price',
                    contains_ssn=False
                ),
                Report(
                    title='Occupancy and Collection',
                    category='Daily',
                    description='',
                    filter_string='',
                    filter_values='',
                    contains_ssn=False
                ),
                Report(
                    title='Trial Bank Deposit',
                    category='Daily',
                    description='',
                    filter_string='',
                    filter_values='',
                    contains_ssn=False
                ),
                Report(
                    title='Credit Cards - ACH to Deposit',
                    category='Daily',
                    description='',
                    filter_string='',
                    filter_values='',
                    contains_ssn=False
                ),
                Report(
                    title='Collections Analysis',
                    category='Daily',
                    description='',
                    filter_string='',
                    filter_values='',
                    contains_ssn=False
                ),
                Report(
                    title='Delinquency',
                    category='Main',
                    description='Delinquency Menu',
                    filter_string='',
                    filter_values='',
                    contains_ssn=False
                ),
                Report(
                    title='Delinquent Rents',
                    category='Delinquency',
                    description='Report of the tenant histories',
                    filter_string='select id, created, tenant_id, user_id, category_id, field_changed, new_value\
                    from tenanthistories',
                    filter_values='tenanthistories;id;created;tenant_id;user_id;category_id;field_changed;\
                    new_value',
                    contains_ssn=False
                ),
                Report(
                    title='Locks to Add',
                    category='Delinquency',
                    description='',
                    filter_string='',
                    filter_values='',
                    contains_ssn=False
                ),
                Report(
                    title='Locks to Remove',
                    category='Delinquency',
                    description='',
                    filter_string='',
                    filter_values='',
                    contains_ssn=False
                ),
                Report(
                    title='Reminder Calls',
                    category='Delinquency',
                    description='',
                    filter_string='',
                    filter_values='',
                    contains_ssn=False
                ),
                Report(
                    title='Charges Waived',
                    category='Delinquency',
                    description='',
                    filter_string='',
                    filter_values='',
                    contains_ssn=False
                ),
                Report(
                    title='Occupancy',
                    category='Main',
                    description='Occupancy Menu',
                    filter_string='',
                    filter_values='',
                    contains_ssn=False
                ),
                Report(
                    title='Unit Summary',
                    category='Occupancy',
                    description='Report of the units.',
                    filter_string='select identifier, tenant_id, size_id from units',
                    filter_values='units;identifier;tenant_id;size_id',
                    contains_ssn=False
                ),
                Report(
                    title='Vacations by Type',
                    category='Occupancy',
                    description='',
                    filter_string='',
                    filter_values='',
                    contains_ssn=False
                ),
                Report(
                    title='Vacations by Size',
                    category='Occupancy',
                    description='',
                    filter_string='',
                    filter_values='',
                    contains_ssn=False
                ),
                Report(
                    title='Three Available',
                    category='Occupancy',
                    description='',
                    filter_string='',
                    filter_values='',
                    contains_ssn=False
                ),
                Report(
                    title='Move In Analysis',
                    category='Occupancy',
                    description='',
                    filter_string='',
                    filter_values='',
                    contains_ssn=False
                ),
                Report(
                    title='Lock and Damaged Checklist',
                    category='Occupancy',
                    description='',
                    filter_string='',
                    filter_values='',
                    contains_ssn=False
                ),
                Report(
                    title='Expected Move Outs',
                    category='Occupancy',
                    description='',
                    filter_string='',
                    filter_values='',
                    contains_ssn=False
                ),
                Report(
                    title='Collections',
                    category='Main',
                    description='Collections Menu',
                    filter_string='',
                    filter_values='',
                    contains_ssn=False
                ),
                Report(
                    title='Month End Analysis',
                    category='Collections',
                    description='Report of the reports',
                    filter_string='select id, title, category, description, contains_ssn from reports',
                    filter_values='reports;id;title;category;description;contains_ssn',
                    contains_ssn=False
                ),
                Report(
                    title='Percent Income by Type',
                    category='Collections',
                    description='',
                    filter_string='',
                    filter_values='',
                    contains_ssn=False
                ),
                Report(
                    title='Revenue per Unit Type',
                    category='Collections',
                    description='',
                    filter_string='',
                    filter_values='',
                    contains_ssn=False
                ),
                Report(
                    title='Remote (web) Payments',
                    category='Collections',
                    description='',
                    filter_string='',
                    filter_values='',
                    contains_ssn=False
                ),
                Report(
                    title='Non-Tenant Collections',
                    category='Collections',
                    description='',
                    filter_string='',
                    filter_values='',
                    contains_ssn=False
                )
            ])
        # -------------------------------------------------------------------------------------
        # Create default unit size categories
        if self.session.query(UnitCategory).count() == 0:
            self.session.add_all([UnitCategory(
                category="Indoor",
                cat_format="{width}x{length}"),
                UnitCategory(
                    category="Outdoor",
                    cat_format="{length} ft."
                )])
        # Create default unit sizes
        if self.session.query(UnitRule).count() == 0:
            self.session.add_all([UnitRule(
                category_id=self.UnitModel.get_category_id("Indoor"),
                length=5,
                width=5,
                floor=0,
                price="40.00"),
                UnitRule(
                    category_id=self.UnitModel.get_category_id("Indoor"),
                    length=10,
                    width=5,
                    floor=0,
                    price="64.00"),
                UnitRule(
                    category_id=self.UnitModel.get_category_id("Indoor"),
                    length=20,
                    width=10,
                    floor=0,
                    price="124.00"),
                UnitRule(
                    category_id=self.UnitModel.get_category_id("Indoor"),
                    length=25,
                    width=10,
                    floor=0,
                    price="134.00"),
                UnitRule(
                    category_id=self.UnitModel.get_category_id("Outdoor"),
                    length=20,
                    width=10,
                    floor=0,
                    price="40.00"),
                UnitRule(
                    category_id=self.UnitModel.get_category_id("Outdoor"),
                    length=35,
                    width=10,
                    floor=0,
                    price="55.00"),
                UnitRule(
                    category_id=self.UnitModel.get_category_id("Outdoor"),
                    length=40,
                    width=10,
                    floor=0,
                    price="70.00")
            ])
        # Create default business rules
        if self.session.query(BusinessRule).count() == 0:
            self.session.add_all([
                BusinessRule(
                    rule="Website",
                    value="https://"
                ),
                BusinessRule(
                    rule="Due Day",
                    value="1"
                ),
                BusinessRule(
                    rule="Late Day",
                    value="11"
                ),
                BusinessRule(
                    rule="Lien Day",
                    value="18"
                ),
                BusinessRule(
                    rule="Sales Tax",
                    value="6.85"
                ),
            ])
        # Create default transaction categories
        if self.session.query(TransactionCategory).count() == 0:
            self.session.add_all([
                TransactionCategory(category="Unit"),
                TransactionCategory(category="Tenant"),
                TransactionCategory(category="Deposits"),
                TransactionCategory(category="Late Fee"),
                TransactionCategory(category="Pre Lien Fee"),
                TransactionCategory(category="Lien Fee"),
                TransactionCategory(category="Advertisement Fee"),
                TransactionCategory(category="Auction Lock Fee"),
                TransactionCategory(category="Lock Cut Fee"),
                TransactionCategory(category="Inventory"),
                TransactionCategory(category="Tax")
            ])
        # Create default history categories
        if self.session.query(HistoryCategory).count() == 0:
            self.session.add_all([
                HistoryCategory(category="Note"),
                HistoryCategory(category="Update"),
                HistoryCategory(category="Reservation"),
                HistoryCategory(category="Reservation Cancel"),
                HistoryCategory(category="Move In"),
                HistoryCategory(category="Move Out"),
                HistoryCategory(category="Late Notice"),
                HistoryCategory(category="Pre Lien"),
                HistoryCategory(category="Lien"),
                HistoryCategory(category="Auction"),
                HistoryCategory(category="Phone Outgoing"),
                HistoryCategory(category="Phone Incoming"),
                HistoryCategory(category="Email Outgoing"),
                HistoryCategory(category="Email Incoming"),
                HistoryCategory(category="Letter Outgoing"),
                HistoryCategory(category="Letter Incoming")
            ])
        self.session.commit()

    def new(self, item):
        """Creates a new database item, setting order in case of Unit items. This works for any item type."""
        # Add order value to new unit
        if type(item) == Unit:
            order_val = self.session.query(func.max(Unit.order)).one()
            # Check to see if any unit values exist
            if order_val[0]:
                order_val = 1 + order_val[0]
            else:
                order_val = 1
            item.order = order_val
        try:
            self.session.add(item)
            self.session.commit()
        except DatabaseError:
            # For now assume unique error if unit type
            if type(item) == Unit:
                return "err_unique"
        return item.id

    def wipe(self):
        """Deletes and recreates database"""
        if os.path.exists(self.filename):
            self.session.close()
            self.engine.dispose()
            os.remove(self.filename)
            self.load(self.filename)
