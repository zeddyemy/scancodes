from enum import Enum

class QRCodeType(Enum):
    MENU    = "menu"
    CARD    = "card"
    PAYMENT = "payment"
    CUSTOM  = "custom"
