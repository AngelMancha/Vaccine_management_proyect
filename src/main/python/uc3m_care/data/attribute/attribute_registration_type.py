"""Classs for the attribute PhoneNumber"""
from uc3m_care.data.attribute.attribute import Attribute

#pylint: disable=too-few-public-methods
class RegistrationType(Attribute):
    """Classs for the attribute PhoneNumber"""
    _validation_pattern = r"(Regular|Family)"
    _validation_error_message = "Registration type is nor valid"
