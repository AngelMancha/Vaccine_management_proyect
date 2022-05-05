"""Subclass of JsonParer for parsing inputs of get_vaccine_date"""
from uc3m_care.parser.json_parser import JsonParser

class AppointmentJsonParser(JsonParser):
    """Subclass of JsonParer for parsing inputs of get_vaccine_date"""
    BAD_PHONE_NUMBER_LABEL_ERROR = "Bad label contact phone"
    BAD_PATIENT_SYS_ID_LABEL_ERROR = "Bad label patient_id"
    PATIENT_SYSTEM_ID_KEY = "PatientSystemID"
    CONTACT_PHONE_NUMBER_KEY = "ContactPhoneNumber"

    _JSON_KEYS = [ PATIENT_SYSTEM_ID_KEY, CONTACT_PHONE_NUMBER_KEY ]
    _ERROR_MESSAGES = [ BAD_PATIENT_SYS_ID_LABEL_ERROR, BAD_PHONE_NUMBER_LABEL_ERROR ]
