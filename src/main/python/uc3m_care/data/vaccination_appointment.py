"""Contains the class Vaccination Appointment"""
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
from uc3m_care.parser.appointment_json_parser import AppointmentJsonParser
from uc3m_care.vaccine_manager import VaccineManager

from uc3m_care import JSON_FILES_PATH
import json
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

#pylint: disable=too-many-instance-attributes
class VaccinationAppointment():
    """Class representing an appointment  for the vaccination of a patient"""

    def __init__(self, patient_sys_id, patient_phone_number, input_date):
        self.__alg = "SHA-256"
        self.__type = "DS"
        self.__patient_sys_id = PatientSystemId(patient_sys_id).value
        patient = VaccinePatientRegister.create_patient_from_patient_system_id(
            self.__patient_sys_id)
        self.__patient_id = patient.patient_id
        self.__phone_number = PhoneNumber(patient_phone_number).value
        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)

        #timestamp is represneted in seconds.microseconds
        #age must be expressed in senconds to be added to the timestap
        print("La fecha ", input_date)
        self.__appointment_date = datetime.timestamp(datetime.fromisoformat(input_date))
        self.__date_signature = self.vaccination_signature



    def __signature_string(self):
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + self.__alg +",typ:" + self.__type +",patient_sys_id:" + \
               self.__patient_sys_id + ",issuedate:" + self.__issued_at.__str__() + \
               ",vaccinationtiondate:" + self.__appointment_date.__str__() + "}"

    @property
    def patient_id( self ):
        """Property that represents the guid of the patient"""
        return self.__patient_id

    @patient_id.setter
    def patient_id( self, value ):
        self.__patient_id = value

    @property
    def patient_sys_id(self):
        """Property that represents the patient_sys_id of the patient"""
        return self.__patient_sys_id
    @patient_sys_id.setter
    def patient_sys_id(self, value):
        self.__patient_sys_id = value

    @property
    def phone_number( self ):
        """Property that represents the phone number of the patient"""
        return self.__phone_number

    @phone_number.setter
    def phone_number( self, value ):
        self.__phone_number = PhoneNumber(value).value

    @property
    def vaccination_signature( self ):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()

    @property
    def issued_at(self):
        """Returns the issued at value"""
        return self.__issued_at

    @issued_at.setter
    def issued_at( self, value ):
        self.__issued_at = value

    @property
    def appointment_date( self ):
        """Returns the vaccination date"""
        return self.__appointment_date

    @property
    def date_signature(self):
        """Returns the SHA256 """
        return self.__date_signature

    def save_appointment( self ):
        """saves the appointment in the appointments store"""
        appointments_store = AppointmentsJsonStore()
        appointments_store.add_item(self)


    @classmethod
    def get_appointment_from_date_signature( cls, date_signature, date):
        """returns the vaccination appointment object for the date_signature received"""
        appointments_store = AppointmentsJsonStore()
        appointment_record = appointments_store.find_item(DateSignature(date_signature).value)
        if appointment_record is None:
            raise VaccineManagementException("date_signature is not found")
        freezer = freeze_time(
            datetime.fromtimestamp(appointment_record["_VaccinationAppointment__issued_at"]))
        freezer.start()
        appointment = cls(appointment_record["_VaccinationAppointment__patient_sys_id"],
                          appointment_record["_VaccinationAppointment__phone_number"],date)
        freezer.stop()
        return appointment

    @classmethod
    def create_appointment_from_json_file( cls, json_file, date ):
        """returns the vaccination appointment for the received input json file"""
        #VaccinationAppointment.check_date(VaccinationAppointment(), date)

        try:
            datetime.fromisoformat(date)
        except ValueError:
            raise VaccineManagementException("Incorrect ISO format")

        current_date = datetime.today().isoformat()
        if date <= current_date:
            raise VaccineManagementException("The date has to be greater than today")

        appointment_parser = AppointmentJsonParser(json_file)

        new_appointment = cls(
            appointment_parser.json_content[appointment_parser.PATIENT_SYSTEM_ID_KEY], appointment_parser.json_content[appointment_parser.CONTACT_PHONE_NUMBER_KEY], date)

        return new_appointment

    def check_date(self, date):
        """Checks that the date has the correct format and it has a correct value"""
        # check that the date is isoformat
        try:
            datetime.fromisoformat(date)
        except ValueError:
            raise VaccineManagementException("Incorrect ISO format")

        current_date = datetime.today().isoformat()
        if date <= current_date:
            raise VaccineManagementException("The date has to be greater than today")
        else:
            return True

    def cancelation_appointment(self, input_file):
        file_cancel_date = JSON_FILES_PATH + "cancel_appointment.json"
        # first read the file
        try:
            with open(file_cancel_date, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except json.JSONDecodeError as ex:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from ex
        except FileNotFoundError as ex:
            raise VaccineManagementException("Store_date not found") from ex

        file_store_date = JSON_FILES_PATH + "store_date.json"
        # first read the file
        try:
            with open(file_store_date, "r", encoding="utf-8", newline="") as file:
                store_date = json.load(file)
        except json.JSONDecodeError as ex:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from ex
        except FileNotFoundError as ex:
            raise VaccineManagementException("Store_date not found") from ex

        found = False
        for item in store_date:
            if item["_VaccinationAppointment__date_signature"] == data_list["date_signature"]:
                found = True
                vaccination_date = item["_VaccinationAppointment__appointment_date"]

                today = freeze_time(datetime.today().timestamp())
                today.start()
                if vaccination_date < today:
                    raise VaccineManagementException("The appointment has already passed")
                today.stop()
        vaccination_date = datetime.fromtimestamp(vaccination_date).isoformat()
        if not found:
            raise VaccineManagementException("Appointment not found")
        date_signature = data_list["date_signature"]
        boolean = VaccineManager.vaccine_patient(date_signature, vaccination_date)
        if boolean:
            raise VaccineManagementException("The vaccine has already been administered")
        return date_signature


    def is_valid_today( self ):
        """returns true if today is the appointment's date"""
        today = datetime.today().date()
        date_patient = datetime.fromtimestamp(self.appointment_date).date()
        if date_patient != today:
            raise VaccineManagementException("Today is not the date")
        return True

    def register_vaccination( self ):
        """register the vaccine administration"""
        if self.is_valid_today():
            vaccination_log_entry = VaccinationLog(self.date_signature)
            vaccination_log_entry.save_log_entry()
        return True
