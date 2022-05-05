"""Tests for singleton patter"""

import unittest
from uc3m_care import VaccineManager
from uc3m_care.storage.vaccination_json_store import VaccinationJsonStore
from uc3m_care.storage.patients_json_store import PatientsJsonStore
from uc3m_care.storage.appointments_json_store import AppointmentsJsonStore

class MyTestCase(unittest.TestCase):
    """Tests for singleton pattern"""
    def test_vaccine_manager_singleton ( self ):
        """testing singleton for VaccineManager"""
        vm1 = VaccineManager()
        vm2 = VaccineManager()
        vm3 = VaccineManager()
        vm4 = VaccineManager()

        self.assertEqual(id(vm1), id(vm2))
        self.assertEqual(id(vm1), id(vm3))
        self.assertEqual(id(vm1), id(vm4))

    def test_patients_store_singleton ( self ):
        """testing singleton for PatientsJsonStore"""
        vm1 = PatientsJsonStore()
        vm2 = PatientsJsonStore()
        vm3 = PatientsJsonStore()
        vm4 = PatientsJsonStore()

        self.assertEqual(id(vm1), id(vm2))
        self.assertEqual(id(vm1), id(vm3))
        self.assertEqual(id(vm1), id(vm4))

    def test_appointments_store_singleton ( self ):
        """testing singleton for AppointmentsJsonStore"""
        vm1 = AppointmentsJsonStore()
        vm2 = AppointmentsJsonStore()
        vm3 = AppointmentsJsonStore()
        vm4 = AppointmentsJsonStore()

        self.assertEqual(id(vm1), id(vm2))
        self.assertEqual(id(vm1), id(vm3))
        self.assertEqual(id(vm1), id(vm4))

    def test_vaccination_store_singleton ( self ):
        """testing singleton for VaccinationJsonStore"""
        vm1 = VaccinationJsonStore()
        vm2 = VaccinationJsonStore()
        vm3 = VaccinationJsonStore()
        vm4 = VaccinationJsonStore()

        self.assertEqual(id(vm1), id(vm2))
        self.assertEqual(id(vm1), id(vm3))
        self.assertEqual(id(vm1), id(vm4))

if __name__ == '__main__':
    unittest.main()
