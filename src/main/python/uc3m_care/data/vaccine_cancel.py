"""Contains the class Cancel Appointment"""
from datetime import datetime
import hashlib
from pathlib import Path
import json
from freezegun import freeze_time

from uc3m_care import VaccinationAppointment
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


        vaccination_date = appointment_record["_VaccinationAppointment__appointment_date"]
        # check the date

        self.check_date_cancel(vaccination_date)

        """
        appointment_administration = VaccinationJsonStore()
        appointment_admin_rec = appointment_administration.find_item(self.__date_signature)
        if appointment_admin_rec is not None:
            raise VaccineManagementException("Vaccination has already been administered")
        """

        already_canceled = self.check_if_canceled(self.__date_signature)
        if already_canceled is True:
            raise VaccineManagementException("Vaccination has already been canceled")


        #check if the appointment has been canceled with store_cancelation.json
        """
        cancelation_store = CancelationJsonStore()
        cancel_record = cancelation_store.find_item(self.__date_signature)
        if cancel_record is not None:
            raise VaccineManagementException("Vaccination has already been canceled")
            """

        #cancel de appointment
        self.cancelation_appointment(self.__date_signature, self.__cancelation_type)


        # save the canceled appointment in a json_file
        #self.save_store_cancel(self.__date_signature, self.__reason)


    def cancelation_appointment(self, date_signature, cancelation_type):

        file_store_date = str(Path.home()) + "/PycharmProjects/G88.2022.T05.FP/src/JsonFiles/" + "store_date.json"
        # first read the file
        try:
            with open(file_store_date, "r", encoding="utf-8", newline="") as file:
                store_date = json.load(file)
        except json.JSONDecodeError as ex:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from ex
        except FileNotFoundError as ex:
            raise VaccineManagementException("Store_date not found") from ex

        for item in store_date:
            if item["_VaccinationAppointment__date_signature"] == date_signature:

                if cancelation_type == "Final":
                    store_date.remove(item)
                    b_file = open(file_store_date, "w")
                    json.dump(store_date, b_file)
                    b_file.close()

                if cancelation_type == "Temporal":
                    item["Cancelation"] = "CONFIRMED"
                    a_file = open(file_store_date, "w")
                    json.dump(store_date, a_file)
                    a_file.close()

    """
    def save_store_cancel(self, date_signature, reason):
        file_store_cancelation = str(Path.home()) + "/PycharmProjects/G88.2022.T05.FP/src/JsonFiles/" + "final_cancel.json"
        # first read the file
        try:
            with open(file_store_cancelation, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            data_list = []
        except json.JSONDecodeError as ex:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from ex

        # append the date
        data_list.append(date_signature.__str__())
        data_list.append(reason.__str__())
        try:
            with open(file_store_cancelation, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise VaccineManagementException("Wrong file or file path") from ex
        return True

        """

    def check_if_canceled(self, date_signature):
            file_store_cancelation = str(Path.home()) + "/PycharmProjects/G88.2022.T05.FP/src/JsonFiles/" + "store_cancelation.json"
            try:
                with open(file_store_cancelation, "r", encoding="utf-8", newline="") as file:
                    data_list = json.load(file)
            except FileNotFoundError:
                # file is not found , so  init my data_list
                data_list = []
            except json.JSONDecodeError as ex:
                raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from ex

            for item in data_list:
                if item["_VaccineCancelation__date_signature"]==date_signature:
                     return True

            return False


