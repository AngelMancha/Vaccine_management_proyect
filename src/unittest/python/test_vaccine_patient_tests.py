"""Module for testing vaccine_patient"""
import unittest
from unittest import TestCase
from freezegun import freeze_time
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from uc3m_care import JSON_FILES_RF2_PATH
from uc3m_care.storage.vaccination_json_store import VaccinationJsonStore
from uc3m_care.storage.appointments_json_store import AppointmentsJsonStore
from uc3m_care.storage.patients_json_store import PatientsJsonStore

class TestVaccinePatient(TestCase):
    """Class for testing vaccine patient"""
    @freeze_time("2022-03-08")
    def setUp(self):
        """first prepare the stores"""

        file_store_patient = PatientsJsonStore()
        file_store_date = AppointmentsJsonStore()

        file_store_date.delete_json_file()
        file_store_patient.delete_json_file()
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        #add patient and date in the store
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima", "Regular",
                                          "+34123456789", "6")
        my_manager.get_vaccine_date(file_test)

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax", "Family",
                                          "+34333456789","7")
        file_test = JSON_FILES_RF2_PATH + "test_ok_2.json"

        my_manager.get_vaccine_date(file_test)

    @freeze_time("2022-03-18")
    def test_vaccine_patient_ok(self):
        """basic path , signature is found , and date = today"""
        my_manager = VaccineManager()
        value = my_manager.vaccine_patient\
                ("5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        self.assertTrue(value)
        vaccination_log = VaccinationJsonStore()
        vaccination_entry = vaccination_log.find_item\
            ("5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        self.assertIsNotNone(vaccination_entry)


    @freeze_time("2022-04-18")
    def test_vaccine_patient_no_date(self):
        """path signature is found , and date is not today"""
        file_store_vaccine = VaccinationJsonStore()
        file_store_vaccine.delete_json_file()
        my_manager = VaccineManager()


        # read the file  to compare
        hash_original = file_store_vaccine.data_hash()

        with self.assertRaises(VaccineManagementException) as context_manager:
            my_manager.vaccine_patient(
                "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        self.assertEqual(context_manager.exception.message, "Today is not the date")
        # read the file again to compare
        hash_new = file_store_vaccine.data_hash()

        self.assertEqual(hash_new, hash_original)

    @freeze_time("2022-03-18")
    def test_vaccine_patient_bad_date_signature(self):
        """path signature is not valid format , only 63 chars"""
        file_store_vaccine = VaccinationJsonStore()
        my_manager = VaccineManager()
        # read the file  to compare
        hash_original = file_store_vaccine.data_hash()
        with self.assertRaises(VaccineManagementException) as context_manager:
            my_manager.vaccine_patient(
                "a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        self.assertEqual(context_manager.exception.message, "date_signature format is not valid")
        hash_new = file_store_vaccine.data_hash()

        self.assertEqual(hash_new, hash_original)

    @freeze_time("2022-03-18")
    def test_vaccine_patient_not_found_date_signature(self):
        """path: signature is not found in store_date"""
        file_store_vaccine = VaccinationJsonStore()
        my_manager = VaccineManager()
        # read the file  to compare
        hash_original = file_store_vaccine.data_hash()

        with self.assertRaises(VaccineManagementException) as context_manager:
            my_manager.vaccine_patient(
                "7a8403d8605804cf2534fd7885940f3c3d8ec60ba578bc158b5dc2b9fb68d524")
        self.assertEqual(context_manager.exception.message, "date_signature is not found")
        # read the file again to compare
        hash_new = file_store_vaccine.data_hash()
        self.assertEqual(hash_new, hash_original)


    @freeze_time("2022-03-18")
    @unittest.skip("This exception won't be raised after the refactoring process")
    def test_vaccine_patient_no_store_date(self):
        """path: store_date is not found, so remove store_date.json"""
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        my_manager = VaccineManager()
        with self.assertRaises(VaccineManagementException) as context_manager:
            my_manager.vaccine_patient(
                "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        self.assertEqual(context_manager.exception.message, "Store_date not found")

    @freeze_time("2022-03-18")
    def test_vaccine_patient_store_date_is_empty(self):
        """for testing: store_date is empty"""
        #write a store_date empty
        file_store_date = AppointmentsJsonStore()
        file_store_date.empty_json_file()
        my_manager = VaccineManager()
        with self.assertRaises(VaccineManagementException) as context_manager:
            my_manager.vaccine_patient(
                "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        self.assertEqual(context_manager.exception.message, "date_signature is not found")
