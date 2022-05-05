"""Subclass of JsonStore for managing the VaccinationLog"""

from uc3m_care.storage.json_store import JsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

class VaccinationJsonStore():
    """Implmentation of the singleton pattern"""
    #pylint: disable=invalid-name
    class __VaccinationJsonStore(JsonStore):
        """Subclass of JsonStore for managing the VaccinationLog"""
        _FILE_PATH = JSON_FILES_PATH + "store_vaccine.json"
        _ID_FIELD = "_VaccinationLog__date_signature"

        def add_item( self, item ):
            """Overrides the add_item to verify the item to be stored"""
            #pylint: disable=import-outside-toplevel, cyclic-import
            from uc3m_care.data.vaccination_log import VaccinationLog
            if not isinstance(item, VaccinationLog):
                raise VaccineManagementException("Invalid VaccinationLog object")
            super().add_item(item)

    instance = None
    def __new__ ( cls ):
        if not VaccinationJsonStore.instance:
            VaccinationJsonStore.instance = VaccinationJsonStore.__VaccinationJsonStore()
        return VaccinationJsonStore.instance

    def __getattr__ ( self, nombre ):
        return getattr(self.instance, nombre)

    def __setattr__ ( self, nombre, valor ):
        return setattr(self.instance, nombre, valor)
