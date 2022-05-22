"""Class representing an entry of the vaccine cancelation log"""
from datetime import datetime
from uc3m_care.storage.file_cancel_json_store import CancelationJsonStore

#pylint: disable=too-few-public-methods
class CancelationLog():
    """Class representing an entry of the Vaccine administration log"""

    def __init__(self, date_signature, cancelation_type, reason):
        self.__date_signature = date_signature
        self.__cancelation_type = cancelation_type
        self.__reason = reason

    def save_log_entry( self ):
        """saves the entry in the vaccine administration log"""
        vaccination_log = CancelationJsonStore()
        vaccination_log.add_item(self)

    @property
    def date_signature( self ):
        """returns the value of the date_signature"""
        return self.__date_signature

    @property
    def cancelation_type( self ):
        """returns the timestamp corresponding to the date of administration """
        return self.__cancelation_type

    @property
    def reason(self):
        return self.__reason