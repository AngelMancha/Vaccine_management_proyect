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

class TestCncelAppointment(TestCase):

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
    def test_something(self):
        self.assertEqual(True, False)



