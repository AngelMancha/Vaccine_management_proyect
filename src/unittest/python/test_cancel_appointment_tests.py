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

param_list_nok = [("test_dup_all.json", "JSON Decode Error - Wrong JSON Format"), # bien
                  ("test_dup_content.json", "JSON Decode Error - Wrong JSON Format"),

                  ("test_dup_date_sig.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_final_bracket.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_final_quote.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_hex.json", "patient system id is not valid"),
                  ("test_dup_init_quote.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_initial_bracket.json", "phone number is not valid"),
                  ("test_dup_rea.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_rn.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_sep1.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_sep2.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_sep_2.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_value_d1.json", "Bad label patient_id"),
                  ("test_dup_value_d2.json", "JSON Decode Error - Wrong JSON Format"),


                  # continuar aqui
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

# ("test_dup_cn.json", "phone number is not valid"),
# ("test_dup_ct.json", "JSON Decode Error - Wrong JSON Format"),
class TestCncelAppointment(TestCase):
    """Class for testing the cancel_vaccine method"""
    @freeze_time("2022-03-08")
    def test_cancel_vaccine_ok(self):
        """test ok"""
        file_test_cancel = JSON_FILES_RF3_PATH + "cancel_appointment_ok.json"
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()
        # date = "2023-04-06"
        date = "2022-03-18"
        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        # check the method
        my_manager.get_vaccine_date(file_test, date)  # añadir date
        value = my_manager.cancel_appointment(file_test_cancel)
        self.assertEqual(value, "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")


    def test_cancel_vaccine_no_ok_not_exist(self):
        file_test = JSON_FILES_RF3_PATH + "cancel_appointment_not_exist.json"
        my_manager = VaccineManager()
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual(c_m.exception.message, "Appointment not found")

    @freeze_time("2023-03-08")
    def test_cancel_vaccine_no_ok_passed(self):
        file_test = JSON_FILES_RF3_PATH + "cancel_appointment_passed.json"
        my_manager = VaccineManager()
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual(c_m.exception.message, "The appointment has already passed")

    @freeze_time("2022-03-08")
    def test_cancel_vaccine_no_ok_canceled(self):
        file_test = JSON_FILES_RF3_PATH + "cancel_appointment_ok.json"
        self.test_cancel_vaccine_ok()
        my_manager = VaccineManager()
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual(c_m.exception.message, "This appointment is already canceled")


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



