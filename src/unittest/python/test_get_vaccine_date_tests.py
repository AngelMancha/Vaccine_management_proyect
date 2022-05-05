"""Tests for get_vaccine_date method"""
from unittest import TestCase
import os
import shutil
from freezegun import freeze_time
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from uc3m_care import JSON_FILES_PATH, JSON_FILES_RF2_PATH
from uc3m_care import AppointmentsJsonStore
from uc3m_care import PatientsJsonStore


param_list_nok = [("test_dup_all.json","JSON Decode Error - Wrong JSON Format"),
                    ("test_dup_char_plus.json","phone number is not valid"),
                    ("test_dup_colon.json","JSON Decode Error - Wrong JSON Format"),
                    ("test_dup_comillas.json","JSON Decode Error - Wrong JSON Format"),
                    ("test_dup_comma.json","JSON Decode Error - Wrong JSON Format"),
                    ("test_dup_content.json","JSON Decode Error - Wrong JSON Format"),
                    ("test_dup_data1.json","JSON Decode Error - Wrong JSON Format"),
                    ("test_dup_data1_content.json","patient system id is not valid"),
                    ("test_dup_data2.json","JSON Decode Error - Wrong JSON Format"),
                    ("test_dup_data2_content.json","phone number is not valid"),
                    ("test_dup_field1.json","JSON Decode Error - Wrong JSON Format"),
                    ("test_dup_field2.json","JSON Decode Error - Wrong JSON Format"),
                    ("test_dup_final_bracket.json","JSON Decode Error - Wrong JSON Format"),
                    ("test_dup_initial_bracket.json","JSON Decode Error - Wrong JSON Format"),
                    ("test_dup_label1.json","JSON Decode Error - Wrong JSON Format"),
                    ("test_dup_label1_content.json","Bad label patient_id"),
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
                    ("test_no_comillas.json","JSON Decode Error - Wrong JSON Format"),
                    ("test_no_phone.json", "phone number is not valid")
                    ]

class TestGetVaccineDate(TestCase):
    """Class for testing get_vaccine_date"""
    @freeze_time("2022-03-08")
    def test_get_vaccine_date_ok(self):
        """test ok"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

    #first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()

    # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular","+34123456789","6")
    #check the method
        value = my_manager.get_vaccine_date(file_test)
        self.assertEqual(value, "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
    #check store_date
        self.assertIsNotNone(file_store_date.find_item(value))

    @freeze_time("2022-03-08")
    def test_get_vaccine_date_no_ok_parameter(self):
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
        for file_name,expected_value in param_list_nok:
            with self.subTest(test=file_name):
                file_test = JSON_FILES_RF2_PATH + file_name
                hash_original = file_store_date.data_hash()

                # check the method
                with self.assertRaises(VaccineManagementException) as c_m:
                    my_manager.get_vaccine_date(file_test)
                self.assertEqual(c_m.exception.message, expected_value)

                # read the file again to compare
                hash_new = file_store_date.data_hash()

                self.assertEqual(hash_new, hash_original)


    @freeze_time("2022-03-08")
    def test_get_vaccine_date_no_ok(self):
        """# long 32 in patient system id , not valid"""
        file_test = JSON_FILES_RF2_PATH + "test_no_ok.json"
        my_manager = VaccineManager()
        file_store_date = AppointmentsJsonStore()

        # read the file to compare file content before and after method call
        hash_original = file_store_date.data_hash()

        #check the method
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.get_vaccine_date(file_test)
        self.assertEqual(c_m.exception.message, "patient system id is not valid")

        # read the file again to campare
        hash_new = file_store_date.data_hash()

        self.assertEqual(hash_new, hash_original)

    @freeze_time("2022-03-08")
    def test_get_vaccine_date_no_ok_no_quotes(self):
        """ no quotes , not valid """
        file_test = JSON_FILES_RF2_PATH + "test_nok_no_comillas.json"
        my_manager = VaccineManager()
        file_store_date = AppointmentsJsonStore()

        # read the file to compare file content before and after method call
        hash_original = file_store_date.data_hash()

    #check the method
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.get_vaccine_date(file_test)
        self.assertEqual(c_m.exception.message, "JSON Decode Error - Wrong JSON Format")

    #read the file again to campare
        hash_new = file_store_date.data_hash()

        self.assertEqual(hash_new, hash_original)


    @freeze_time("2022-03-08")
    def test_get_vaccine_date_no_ok_data_manipulated( self ):
        """ no quotes , not valid """
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()
        file_store = JSON_FILES_PATH + "store_patient.json"
        file_store_date = JSON_FILES_PATH + "store_date.json"

        if os.path.isfile(JSON_FILES_PATH + "swap.json"):
            os.remove(JSON_FILES_PATH + "swap.json")
        if not os.path.isfile(JSON_FILES_PATH + "store_patient_manipulated.json"):
            shutil.copy(JSON_FILES_RF2_PATH + "store_patient_manipulated.json",
                        JSON_FILES_PATH + "store_patient_manipulated.json")

        #rename the manipulated patient's store
        if os.path.isfile(file_store):
            print(file_store)
            print(JSON_FILES_PATH + "swap.json")
            os.rename(file_store, JSON_FILES_PATH + "swap.json")
        os.rename(JSON_FILES_PATH + "store_patient_manipulated.json",file_store)

        file_store_date = AppointmentsJsonStore()
        # read the file to compare file content before and after method call
        hash_original = file_store_date.data_hash()

        # check the method

        exception_message = "Exception not raised"
        try:
            my_manager.get_vaccine_date(file_test)
        #pylint: disable=broad-except
        except Exception as exception_raised:
            exception_message = exception_raised.__str__()

        #restore the original patient's store
        os.rename(file_store, JSON_FILES_PATH + "store_patient_manipulated.json")
        if os.path.isfile(JSON_FILES_PATH + "swap.json"):
            print(JSON_FILES_PATH + "swap.json")
            print(file_store)
            os.rename(JSON_FILES_PATH + "swap.json", file_store)

        # read the file again to campare
        hash_new = file_store_date.data_hash()

        self.assertEqual(exception_message, "Patient's data have been manipulated")
        self.assertEqual(hash_new, hash_original)
