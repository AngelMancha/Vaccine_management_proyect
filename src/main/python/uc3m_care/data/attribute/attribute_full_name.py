"""Classs for the attribute FullName"""
from uc3m_care.data.attribute.attribute import Attribute

#pylint: disable=too-few-public-methods
class FullName(Attribute):
    """Classs for the attribute FullName"""
    _validation_pattern = r"^(?=^.{1,30}$)(([a-zA-Z]+\s)+[a-zA-Z]+)$"
    _validation_error_message = "name surname is not valid"
