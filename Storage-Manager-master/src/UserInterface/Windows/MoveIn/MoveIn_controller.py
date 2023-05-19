"""Code written by Emerson Havener unless otherwise specified."""

from src.UserInterface.Windows.Window.window_controller import WindowController, Err
from .MoveIn_view import MoveInView
from src.UserInterface.Frames.Image_controller import ImageController
from src.DatabaseORM.tenant_orm import Tenant

# TODO: state list is using names, but we want to store as state_id
# TODO: enumerate countries for country list
# TODO: enumerate access times
# TODO: visually indicate when inputs are disabled

# Access times: weekday and hour range
# assume if outdoor unit, enable vehicles


class MoveIn(WindowController):
    def __init__(self, unit):
        self.unit = unit
        self.img_controller = ImageController([], unit)
        super().__init__(MoveInView, "Move In")
        self.load()

    def load(self):
        self.window = self.view.window

    def process_event(self, event, values):
        self.img_controller.process_event(event, values)

        if event in (None, "Cancel"):
            return self.shutdown()
        elif event == "Submit":
            self.submit_tenant(values)
            self.refresh_all()
            return self.shutdown()
        self.setDisabledStates(values)
        return True

    def refresh(self):
        pass

    def shutdown(self):
        self.window.close()
        return False

    def setDisabledStates(self, values):
        if values.get("_COMPANY_"):
            self.window.FindElement('_TAX_ID_').Update(disabled=False)
        else:
            self.window.FindElement('_TAX_ID_').Update(disabled=True)

    # -------------------------------------------------------------------------------------
    # This section coded by Jacquesne Jones
    def submit_tenant(self, values):
        # Check for existing tenant
        if self.existing_tenant(values):
            return False
        # Check for duplicates in alternate
        if (values["_ALT_ADDR1_"] and values["_ADDR1_"] == values["_ALT_ADDR1_"]) or \
                (values["_ALT_ADDR2_"] and values["_ADDR2_"] == values["_ALT_ADDR2_"]) or \
                (values["_ALT_CELL_"] and values["_CELL_"] == values["_ALT_CELL_"]) or \
                (values["_ALT_PHONE_"] and values["_PHONE_"] == values["_ALT_PHONE_"]) or \
                (values["_ALT_EMAIL_"] and values["_EMAIL_"] == values["_ALT_EMAIL_"]):
            raise Err.DuplicateAlternateInfo
        new_tenant = Tenant(
            last=values["_LAST_"],
            first=values["_FIRST_"],
            middle=values["_MIDDLE_"],
            addr1=values["_ADDR1_"],
            addr2=values["_ADDR2_"],
            city=values["_CITY_"],
            state=values["_STATE_ID_"],
            zip=values["_ZIP_"],
            country=values["_COUNTRY_"],
            cell=values["_CELL_"],
            phone=values["_PHONE_"],
            email=values["_EMAIL_"],
            company=values["_COMPANY_"],
            license_num=values["_LICENSE_NUM_"],
            license_state=values["_LICENSE_STATE_"],
            ssn=values["_SSN_"],
            lease=values["_LEASE_"],
            tax_id=values["_TAX_ID_"],
            # TODO: Implement once alternate is added to view
            # alt_relationship=values["_ALT_RELATIONSHIP_"],
            alt_last=values["_ALT_LAST_"],
            alt_first=values["_ALT_FIRST_"],
            alt_middle=values["_ALT_MIDDLE_"],
            alt_addr1=values["_ALT_ADDR1_"],
            alt_addr2=values["_ALT_ADDR2_"],
            alt_city=values["_ALT_CITY_"],
            alt_state=values["_ALT_STATE_"],
            alt_zip=values["_ALT_ZIP_"],
            alt_country=values["_ALT_COUNTRY_"],
            alt_phone=values["_ALT_PHONE_"],
            alt_cell=values["_ALT_CELL_"],
            alt_email=values["_ALT_EMAIL_"],
            gate_code=values["_GATE_CODE_"],
            access_id=values["_ACCESS_"],
            never_lock=values["_NEVER_LOCK_"],
            deactivate_gate=values["_DEACTIVATE_GATE_"],
            web_access=values["_WEB_ACCESS_"],
            vehicle_vin=values["_VEHICLE_VIN_"],
            plate_num=values["_PLATE_NUM_"],
            vehicle_state=values["_VEHICLE_STATE_"],
            insurance_num=values["_INSURANCE_NUM_"],
            lien_holder=values["_LIEN_HOLDER_"],

        )
        self.database.new(new_tenant)
        self.database.UnitModel.move_in(self.unit, new_tenant)
        self.refresh_all()
        return True

    def existing_tenant(self, values):
        """Check if a tenant likely already exists, if so, set tenant to that value."""
        tenant = self.database.TenantModel.get_by_ssn(values["_SSN_"])
        if values["_SSN_"] != "" and tenant:
            if self.popup("This tenant likely already exists. Really create a new tenant?",
                          ["Yes", "Use Existing"]):
                return False
            else:
                self.database.UnitModel.move_in(self.unit, tenant)
    # -------------------------------------------------------------------------------------
