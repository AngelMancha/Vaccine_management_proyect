"""Subclass of JsonStore for managing the cancelations"""
from uc3m_care.storage.json_store import JsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH


class CancelationJsonStore():
    """Implmentation of the singleton pattern"""
    #pylint: disable=invalid-name
    class __CancelationJsonStore(JsonStore):
        """Subclass of JsonStore for managing the VaccinationLog"""
        _FILE_PATH = JSON_FILES_PATH + "store_cancelation.json"
        _ID_FIELD = "_VaccineCancelation__date_signature"

        def add_item( self, item ):
            """Overrides the add_item to verify the item to be stored"""
            #pylint: disable=import-outside-toplevel, cyclic-import
            super().add_item(item)

    instance = None

    def __new__ ( cls ):
        if not CancelationJsonStore.instance:
            CancelationJsonStore.instance = CancelationJsonStore.__CancelationJsonStore()
        return CancelationJsonStore.instance

    def __getattr__ ( self, nombre ):
        return getattr(self.instance, nombre)

    def __setattr__ ( self, nombre, valor ):
        return setattr(self.instance, nombre, valor)
