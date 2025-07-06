from enum import Enum

class QRCodeType(Enum):
    MENU    = "menu"
    CARD    = "card"
    PAYMENT = "payment"
    CUSTOM  = "custom"
    
    def __str__(self) -> str:
        return self.value  # Ensures usage as strings in queries

