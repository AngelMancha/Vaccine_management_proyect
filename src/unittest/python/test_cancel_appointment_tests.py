"""Tests for get_vaccine_date method"""
from unittest import TestCase
import os
import shutil
from freezegun import freeze_time
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from uc3m_care import JSON_FILES_PATH
from uc3m_care import AppointmentsJsonStore
from uc3m_care import PatientsJsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_RF3_PATH, JSON_FILES_RF2_PATH

param_list_nok = [("test_dup_all.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_char_plus.json", "phone number is not valid"),
                  ("test_dup_colon.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_comillas.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_comma.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_content.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_data1.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_data1_content.json", "patient system id is not valid"),
                  ("test_dup_data2.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_data2_content.json", "phone number is not valid"),
                  ("test_dup_field1.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_field2.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_final_bracket.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_initial_bracket.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_label1.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_label1_content.json", "Bad label patient_id"),
                  ("test_dup_label2.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_label2_content.json", "Bad label contact phone"),
                  ("test_dup_phone.json", "phone number is not valid"),
                  ("test_empty.json", "Bad label patient_id"),
                  ("test_mod_char_plus.json", "phone number is not valid"),
                  ("test_mod_data1.json", "patient system id is not valid"),
                  ("test_mod_data2.json", "phone number is not valid"),
                  ("test_mod_label1.json", "Bad label patient_id"),
                  ("test_mod_label2.json", "Bad label contact phone"),
                  ("test_mod_phone.json", "phone number is not valid"),
                  ("test_no_char_plus.json", "phone number is not valid"),
                  ("test_no_colon.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_no_comillas.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_no_phone.json", "phone number is not valid")
                  ]


class TestCncelAppointment(TestCase):
    """Class for testing the cancel_vaccine method"""
    @freeze_time("2022-03-08")
    def test_cancel_vaccine_ok(self):
        """test ok"""
        file_test = JSON_FILES_RF3_PATH + "cancel_appointment_ok.json"

        my_manager = VaccineManager()
        value = my_manager.cancel_appointment(file_test)
        self.assertEqual(value, "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")

    """
    @freeze_time("2022-03-08")
    def test_get_vaccine_date_no_ok_data_manipulated(self):
      
        date = "2022-03-18"
        file_test = JSON_FILES_RF3_PATH + "test_ok.json"
        my_manager = VaccineManager()
        file_store = JSON_FILES_PATH + "store_patient.json"
        file_store_date = JSON_FILES_PATH + "store_date.json"

        if os.path.isfile(JSON_FILES_PATH + "swap.json"):
            os.remove(JSON_FILES_PATH + "swap.json")
        if not os.path.isfile(JSON_FILES_PATH + "store_patient_manipulated.json"):
            shutil.copy(JSON_FILES_RF3_PATH + "store_patient_manipulated.json",
                        JSON_FILES_PATH + "store_patient_manipulated.json")

        # rename the manipulated patient's store
        if os.path.isfile(file_store):
            print(file_store)
            print(JSON_FILES_PATH + "swap.json")
            os.rename(file_store, JSON_FILES_PATH + "swap.json")
        os.rename(JSON_FILES_PATH + "store_patient_manipulated.json", file_store)

        file_store_date = AppointmentsJsonStore()
        # read the file to compare file content before and after method call
        hash_original = file_store_date.data_hash()

        # check the method

        exception_message = "Exception not raised"
        try:
            my_manager.get_vaccine_date(file_test, date)
        # pylint: disable=broad-except
        except Exception as exception_raised:
            exception_message = exception_raised.__str__()

        # restore the original patient's store
        os.rename(file_store, JSON_FILES_PATH + "store_patient_manipulated.json")
        if os.path.isfile(JSON_FILES_PATH + "swap.json"):
            print(JSON_FILES_PATH + "swap.json")
            print(file_store)
            os.rename(JSON_FILES_PATH + "swap.json", file_store)

        # read the file again to campare
        hash_new = file_store_date.data_hash()

        self.assertEqual(exception_message, "Patient's data have been manipulated")
        self.assertEqual(hash_new, hash_original)
        """


