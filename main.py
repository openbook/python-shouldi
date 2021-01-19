from func import *
import pytz, datetime
from functools import reduce

tz = pytz.timezone("Europe/London")

apiBase = "https://api.carbonintensity.org.uk"
apiGeneration = "/generation"
generationMixWanted = ["solar", "wind", "hydro"]
generationLimit = 33

"""
    Get current total renewable gen
"""


def now():
    responseNow = requests.get(apiBase + apiGeneration)
    data = responseNow.json()
    shouldINow = getGenerationMixTotalForSlot(data["data"], generationMixWanted)
    return shouldINow > generationLimit, shouldINow


"""
    Get 5 day forecast
"""


def forecast():
    dataOut = {}
    formatted = {}
    dateNowUTC, dateEndUTC = getStartAndEndDates()
    responseForecast = requests.get(
        apiBase
        + apiGeneration
        + "/"
        + dateNowUTC.isoformat()
        + "/"
        + dateEndUTC.isoformat()
    )
    data = responseForecast.json()

    for d in data["data"]:
        date = datetime.datetime.strptime(d["from"], "%Y-%m-%dT%H:%MZ")
        if date.day < dateNowUTC.day:
            continue
        dateKey = date.strftime("%Y-%m-%d")
        if dateKey not in formatted:
            formatted[dateKey] = {}
        slot = getSlotName(d["from"])
        if not slot:
            continue
        if slot not in formatted[dateKey]:
            formatted[dateKey][slot] = []
        formatted[dateKey][slot].append(
            getGenerationMixTotalForSlot(d, generationMixWanted)
        )

    for day in formatted:
        if day not in dataOut:
            dataOut[day] = {}
        for slot in formatted[day]:
            if slot not in dataOut[day]:
                dataOut[day][slot] = []
            total = sum(formatted[day][slot])
            dataOut[day][slot] = (
                True if total / len(formatted[day][slot]) > generationLimit else False
            )

    return dataOut
