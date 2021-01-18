import json
import requests
import pytz, datetime

tz = pytz.timezone("Europe/London")


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def getGenerationMix(dict, wanted):
    dataout = []
    for d in dict["generationmix"]:
        if d["fuel"] in wanted:
            dataout.append(d)
    return dataout


def getGenerationMixTotal(dataIn):
    return sum(c["perc"] for c in dataIn)


def getGenerationMixTotalForSlot(slotData, wanted):
    genMix = getGenerationMix(slotData, wanted)
    genMixWanted = getGenerationMixTotal(genMix)
    return genMixWanted


def shouldAdjustTimeForBST():
    return (
        True
        if tz.utcoffset(datetime.datetime.now().now()).total_seconds() > 0
        else False
    )


def getStartAndEndDates():
    startHour = 1 if shouldAdjustTimeForBST() else 0
    dateNowUTC = datetime.datetime.now(datetime.timezone.utc).replace(
        hour=startHour, minute=0, second=0, microsecond=0
    )
    dateEndUTC = dateNowUTC + datetime.timedelta(days=5)
    return dateNowUTC, dateEndUTC


def getSlotName(datein):
    adjust = shouldAdjustTimeForBST()
    date = datetime.datetime.strptime(datein, "%Y-%m-%dT%H:%MZ")
    if adjust:
        if date.hour >= 0 and date.hour < 6:
            return "night"
        if date.hour >= 6 and date.hour < 12:
            return "morning"
        if date.hour >= 12 and date.hour < 18:
            return "afternoon"
        if date.hour >= 18 and date.hour <= 23:
            return "evening"
    else:
        if date.hour >= 0 and date.hour < 5:
            return "night"
        if date.hour >= 5 and date.hour < 11:
            return "morning"
        if date.hour >= 11 and date.hour < 17:
            return "afternoon"
        if date.hour >= 17 and date.hour <= 23:
            return "evening"

    return False
