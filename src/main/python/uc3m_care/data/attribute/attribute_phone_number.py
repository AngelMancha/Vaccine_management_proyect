"""Classs for the attribute PhoneNumber"""
from uc3m_care.data.attribute.attribute import Attribute

#pylint: disable=too-few-public-methods
class PhoneNumber(Attribute):
    """Classs for the attribute PhoneNumber"""
    _validation_pattern = r"^(\+)[0-9]{11}"
    _validation_error_message = "phone number is not valid"
