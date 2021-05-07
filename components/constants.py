"""constants to be used"""

SET_TYPE, INPUT_FEEDBACK, INPUT_MESSAGE, TYPE_MESSAGE = range(4)

POLLEN = {
    0: "Hasel",
    1: "Erle",
    2: "Birke",
    3: "Gräser",
    4: "Roggen",
    5: "Beifuß",
    6: "Ambrosia",
    7: "Esche"
}

ADMIN = open("admin.txt", "r").read().strip()

DAY = ["today", "tomorrow", "sunday"]
FORECAST_DAY = ["heutige ", "morgige ", "Sonntags-"]