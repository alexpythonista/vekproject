from enum import StrEnum


class DataFields(StrEnum):
    UID = 'uid'
    PID = 'pid'
    BRAND = 'brand'
    CLICK = 'click'
    ADD_TO_CART = 'add_to_cart'
    PURCHASE = 'purchase'


FIELDS = (
    str(DataFields.UID),
    str(DataFields.PID),
    str(DataFields.BRAND),
    str(DataFields.CLICK),
    str(DataFields.ADD_TO_CART),
    str(DataFields.PURCHASE),
)
FIELDS_TO_SORT = (
    str(DataFields.PURCHASE),
    str(DataFields.ADD_TO_CART),
    str(DataFields.CLICK),
)
SORT_ORDER = (False, False, False)
