from itertools import product
from gettext import gettext as _


class JOURNEY_TYPE:
    __travels = [('G', _("Going")), ('R', _("Returning"))]
    __shifts = [('M', _("morning")), ('A', _("afternoon")), ('E', _("evening")), ('N', _("night"))]
    options = [('NM',"Nothing at moment")] + [(t[0] + s[0], f"{t[1]} at {s[1]}") for t, s in product(__travels, __shifts)]
    default = options[0][0]
    
    @staticmethod
    def _filter_from_url(journey_type: str, journey_shift: str):
        result = None
        if journey_type == "going":
            result = JOURNEY_TYPE.__travels[0]
        elif journey_type == "returning":
            result = JOURNEY_TYPE.__travels[1]
            
        if journey_shift == "morning":
            result += JOURNEY_TYPE.__shifts[0][0]
        elif journey_shift == "afternoon":
            result += JOURNEY_TYPE.__shifts[1][0]
        elif journey_shift == "evening":
            result += JOURNEY_TYPE.__shifts[2][0]
        elif journey_shift == "night":
            result += JOURNEY_TYPE.__shifts[3][0]

        return result


class BUS_STATUS:
    options = [('A', _("Active")), ('I', _("Inactive")), ('M', _("Maintenance"))]
    default = options[0][0]

    @staticmethod
    def _filter_from_url(status):
        result = None

        if status == "active":
            result = JOURNEY_TYPE.options[0]
        elif status == "inactive":
            result = JOURNEY_TYPE.options[1]
        elif status == "maintenance":
            result = JOURNEY_TYPE.options[2]

        return result


LOCATION_STATUS = [
    (0, _("Not reach")),
    (1, _("Passed"))
]

STUDENT_STATUS = [
    (0, _("Not on bus yet")),
    (1, _("Missing")),
    (2, _("Absence with report")),
    (3, _("Student is on the way to school")),
    (4, _("Student is on the way to home")),
    (5, _("Student already reached school")),
    (6, _("Student already reached home")),
]

BUS_ACTION = [
    (0, _("stopped")),
    (1, _("moving on")),
    (2, _("ask for help")),
    (3, _("ask for maintenance"))
]

ROUTE_STATUS = [
    (0, _("Not yet started")),
    (1, _("On the way to school")),
    (2, _("On the way to home")),
]

SCHOOL_SHIFT = [
    (0, _("Morning")),
    (1, _("Afternoon")),
    (2, _("Evening")),
    (3, _("Night")),
]
