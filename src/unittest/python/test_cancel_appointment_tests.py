"""Tests for get_vaccine_date method"""
from unittest import TestCase
from freezegun import freeze_time
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from uc3m_care import AppointmentsJsonStore
from uc3m_care import PatientsJsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_RF3_PATH, JSON_FILES_RF2_PATH
from uc3m_care.storage.file_cancel_json_store import CancelationJsonStore

param_list_nok = [("test_dup_all.json", "JSON Decode Error - Wrong JSON Format"), # bien
                  ("test_dup_content.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_date_sig.json", "File is not found"),
                  ("test_dup_final_bracket.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_final_quote.json", "File is not found"),
                  ("test_dup_init_quote.json", "File is not found"),
                  ("test_dup_initial_bracket.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_dup_sep1.json", "File is not found"),
                  ("test_dup_sep2.json", "File is not found"),
                  ("test_dup_sep_2.json", "File is not found"),
                  ("test_dup_value_d1.json", "File is not found"),
                  ("test_dup_value_d2.json", "File is not found"),
                  ("test_mod_comilla.json", "File is not found"),
                  ("test_mod_initial_quote.json", "File is not found"),
                  ("test_no_date_sig.json", "File is not found"),
                  ("test_no_final_bracket.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_no_final_quote.json", "File is not found"),
                  ("test_no_init_quote.json", "File is not found"),
                  ("test_no_initial_bracket.json", "JSON Decode Error - Wrong JSON Format"),
                  ("test_no_sep1.json", "File is not found"),
                  ("test_no_sep2.json", "File is not found"),
                  ("test_no_sep_2.json", "File is not found"),
                  ("test_no_value_d1.json", "File is not found"),
                  ("test_no_value_d2.json", "File is not found")
                  ]

mod_json_nok = [("test_dup_cn.json", "Wrong JSON"),
                ("test_dup_hex.json", "Wrong JSON"),
                ("test_dup_rea.json", "Wrong JSON"),
                ("test_dup_rn.json", "Wrong JSON"),
                ("test_mod_cn.json", "Wrong JSON"),
                ("test_mod_hex.json", "Wrong JSON"),
                ("test_mod_rea.json", "JWrong JSON"),
                ("test_reason_more100.json", "JWrong JSON"),
                ("test_mod_rn.json", "Wrong JSON"),
                ("test_no_cn.json", "Wrong JSON"),
                ("test_no_hex.json", "Wrong JSON"),
                ("test_no_rea.json", "Wrong JSON"),
                ("test_no_rn.json", "Wrong JSON")
                ]

param_nok = [("test_reason_more_100.json", "Bad label reason"),
             ("test_dup_ct.json", "Bad label cancelation type"),
             ("test_dup_dsig.json", "Bad label date signature"),
             ("test_dup_rea.json", "Bad label reason"),
             ("test_no_hex.json", "date_signature is not found"),
             ("test_no_cn.json", "Vaccination has already been canceled"),
             ("test_no_rn.json", "Vaccination has already been canceled"),
             ("test_mod_dsig.json", "Bad label date signature"),
             ("test_mod_rea.json", "Bad label reason"),
             ("test_mod_ct.json", "Bad label cancelation type"),
             ("test_mod_hex.json", "date_signature is not found"),
             ("test_mod_rn.json", "Vaccination has already been canceled")]

class TestCncelAppointment(TestCase):
    """Class for testing the cancel_vaccine method"""
    @freeze_time("2022-03-08")
    def test_cancel_vaccine_ok(self):
        """test ok for temporal value"""

        file_store_patient = CancelationJsonStore()
        file_store_patient.delete_json_file()

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



    @freeze_time("2022-03-08")
    def test_cancel_vaccine_ok_final(self):
        """test ok for final value"""
        file_store_patient = CancelationJsonStore()
        file_store_patient.delete_json_file()
        file_test_cancel = JSON_FILES_RF3_PATH + "cancel_appointment_ok_final.json"
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
        """test for appointment has not been found"""
        file_test = JSON_FILES_RF3_PATH + "cancel_appointment_not_exist.json"
        my_manager = VaccineManager()
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual(c_m.exception.message, "date_signature is not found")

    @freeze_time("2023-03-08")
    def test_cancel_vaccine_no_ok_passed(self):
        """test to check the validity of the date"""
        self.test_cancel_vaccine_ok() # call this method to cancel the appointment
        file_test_passed = JSON_FILES_RF3_PATH + "cancel_appointment_passed.json"
        my_manager = VaccineManager()
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test_passed)
        self.assertEqual(c_m.exception.message, "The appointment has already passed")

    @freeze_time("2022-03-08")
    def test_cancel_vaccine_no_ok_canceled(self):
        """test that checks if the appointmetn is already canceled"""
        file_test = JSON_FILES_RF3_PATH + "cancel_appointment_ok.json"
        self.test_cancel_vaccine_ok() # call this method to cancel the appointment
        my_manager = VaccineManager()
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual(c_m.exception.message, "Vaccination has already been canceled")


    @freeze_time("2022-03-08")
    def test_cancel_vaccine_no_ok_parameter(self):
        """tests no ok"""
        my_manager = VaccineManager()
        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        self.test_cancel_vaccine_ok()  # call this method to cancel the appointment
        for file_name, expected_value in param_list_nok:
            with self.subTest(test=file_name):
                file_test = JSON_FILES_RF2_PATH + file_name
                file_store_date.data_hash()
                # check the method
                with self.assertRaises(VaccineManagementException) as c_m:
                    my_manager.cancel_appointment(file_test)
                self.assertEqual(c_m.exception.message, expected_value)


    @freeze_time("2022-03-08")
    def test_cancel_vaccine_no_ok_json(self):
        """tests no ok"""
        my_manager = VaccineManager()
        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        self.test_cancel_vaccine_ok()  # call this method to cancel the appointment
        for file_name, expected_value in param_list_nok:
            with self.subTest(test=file_name):
                file_test = JSON_FILES_RF2_PATH + file_name
                file_store_date.data_hash()
                # check the method
                with self.assertRaises(VaccineManagementException) as c_m:
                    my_manager.cancel_appointment(file_test)
                self.assertEqual(c_m.exception.message, expected_value)

    @freeze_time("2022-03-08")
    def test_cancel_vaccine_wrong_value(self):
        """tests no ok"""
        my_manager = VaccineManager()
        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        self.test_cancel_vaccine_ok()  # call this method to cancel the appointment
        for file_name, expected_value in param_nok:
            with self.subTest(test=file_name):
                file_test = JSON_FILES_RF3_PATH + file_name
                file_store_date.data_hash()
                # check the method
                with self.assertRaises(VaccineManagementException) as c_m:
                    my_manager.cancel_appointment(file_test)
                self.assertEqual(c_m.exception.message, expected_value)
