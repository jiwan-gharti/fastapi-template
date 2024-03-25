from enum import Enum


class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    CSR = "CSR"
    INSTRUCTOR = "INSTRUCTOR"
    STUDENT = "STUDENT"


class GenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

