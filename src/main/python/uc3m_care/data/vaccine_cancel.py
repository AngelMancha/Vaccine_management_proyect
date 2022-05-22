"""Contains the class Cancel Appointment"""
from datetime import datetime
import hashlib
from freezegun import freeze_time
from uc3m_care.data.attribute.attribute_phone_number import PhoneNumber
from uc3m_care.data.attribute.attribute_patient_system_id import PatientSystemId
from uc3m_care.data.attribute.attribute_date_signature import DateSignature
from uc3m_care.data.vaccination_log import VaccinationLog
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.storage.appointments_json_store import AppointmentsJsonStore
from uc3m_care.storage.vaccination_json_store import VaccinationJsonStore
from uc3m_care.storage.file_cancel_json_store import CancelationJsonStore
from uc3m_care.parser.appointment_json_parser import AppointmentJsonParser
from uc3m_care.parser.cancel_json_parser import CancelJsonParser

from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

class VaccineCancelation():
    """Class representing an appointment  for the vaccination of a patient"""

    def __init__(self, date_signature, cancelation_type, reason):
        self.__date_signature = date_signature
        self.__cancelation_type = cancelation_type
        self.__reason = reason

    @property
    def date_signature(self):
        """Property that represents the guid of the patient"""
        return self.__date_signature

    @date_signature.setter
    def date_signature(self, value):
        if len(value) != 64:
            raise VaccineManagementException("Not an hexadecimal string")
        self.__patient_id = value

    @property
    def cancelation_type(self):
        """Property that represents the guid of the patient"""
        return self.__date_signature

    @cancelation_type.setter
    def cancelation_type(self, value):
        if value != "Temporal" or value != "Final":
            raise VaccineManagementException("Wrong cancelation type")
        self.__cancelation_type = value

    @property
    def reason(self):
        """Property that represents the guid of the patient"""
        return self.__reason

    @reason.setter
    def reason(self, value):
        if len(value) < 0 or len(value) > 100:
            raise VaccineManagementException("Wrong length for the reason")
        self.__reason = value

    @classmethod
    def cancel_appointment(cls, cancel_file):
        """returns the vaccination appointment for the received input json file"""
        cancel_parser = CancelJsonParser(cancel_file)
        cancel_appointment = cls(
            cancel_parser.json_content[cancel_parser.DATE_SIGNATURE_KEY],
            cancel_parser.json_content[cancel_parser.CANCELATION_TYPE_KEY],
            cancel_parser.json_content[cancel_parser.REASON_KEY])
        return cancel_appointment

    def save_cancelation(self):
        """saves the cancelation in the cancelation store"""
        cancel_store = CancelationJsonStore()
        cancel_store.add_item(self)

    def check_date_cancel(self, date):
        today = "2022-03-08"
        freeze = freeze_time(today)
        # today_timestamp=datetime.timestamp(datetime.fromisoformat("2022-03-08"))
        today_timestamp = datetime.timestamp(datetime.today())
        freeze.start()
        if date < today_timestamp:
            raise VaccineManagementException("The appointment has already passed")
        freeze.stop()

    def confirm_cancelation(self):
        appointment_store = AppointmentsJsonStore()
        appointment_record = appointment_store.find_item(self.__date_signature)
        if appointment_record is None:
            raise VaccineManagementException("date_signature is not found")

        print(appointment_store["_VaccinationAppointment__appointment_date"])
        vaccination_date = appointment_store["_VaccinationAppointment__appointment_date"]
        # check the date
        self.check_date_cancel(vaccination_date)

        appointment_administration = VaccinationJsonStore()
        appointment_admin_rec = appointment_administration.find_item(self.__date_signature)
        if appointment_admin_rec is not None:
            raise VaccineManagementException("Vaccination has already been administered")

        cancelation_store = CancelationJsonStore()
        cancel_record = cancelation_store.find_item(self.__date_signature) # it adds to the store_cancel the date signature
        if cancel_record is not None:
            raise VaccineManagementException("Vaccination has already been canceled")

        # if the cancelation type is temporal
        if self.__cancelation_type == "Temporal":
            appointment_store.add_item(self)

