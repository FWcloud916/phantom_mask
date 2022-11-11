""" utils functions for import data """
import json
import re
from pathlib import Path

from app.schemas.masks import ImportMask, MaskCreate
from app.schemas.open_hours import OpenHoursCreate


def read_json_file(file_path: str) -> dict:
    """read json file"""
    file = Path(file_path)
    if not file.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    try:
        return json.loads(file.read_text(encoding="utf-8"))
    except json.decoder.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON file: {file_path}") from e


def parse_mask(mask: ImportMask) -> MaskCreate:
    """parse mask name"""
    # mask_sample = 'True Barrier (green) (10 per pack)'
    regex = r"^(?P<name>.+?)\s\((?P<color>.+?)\)\s\((?P<quantity>.+?)\sper\spack\)$"
    match = re.match(regex, mask.name)
    if not match:
        raise ValueError(f"Invalid mask name: {mask.name}")
    return MaskCreate(**match.groupdict(), price=mask.price)


def parse_open_hours(open_hours: str) -> list[OpenHoursCreate]:
    """parse opening hours"""
    # open_hours_sample = 'Mon, Wed, Fri 20:00 - 02:00'
    # open_hours_sample_2 = 'Mon - Fri 08:00 - 17:00 / Sat, Sun 08:00 - 12:00'
    hours = [x.strip() for x in open_hours.split("/")]
    result = []
    for hour in hours:
        result += parse_open_scope(hour)
    return result


def parse_open_days(param):
    """parse opening days"""
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    if "," in param:
        return param.split(",")
    if "-" in param:
        scope = param.split("-")
        start = days.index(scope[0].strip())
        end = days.index(scope[1].strip())
        return days[start : end + 1]
    if param in days:
        return [param]
    raise ValueError(f"Invalid opening days: {param}")


def parse_open_scope(open_hour: str) -> list[OpenHoursCreate]:
    """parse opening hours info"""
    # open_hours_sample = 'Mon, Wed, Fri 20:00 - 02:00'
    # open_hours_sample_2 = 'Mon - Fri 08:00 - 17:00'
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    regex = r"^(?P<days>\D+?)\s(?P<open>[\d:]+?)\s-\s(?P<close>[\d:]+?)$"
    match = re.match(regex, open_hour)
    if not match:
        raise ValueError(f"Invalid opening hours: {open_hour}")
    result = match.groupdict()
    open_days = parse_open_days(result["days"])
    open_info = []
    for day in days:
        if day in open_days:
            open_info.append(
                OpenHoursCreate(
                    **{
                        "day": days.index(day),
                        "open_time": result["open"],
                        "close_time": result["close"],
                    }
                )
            )
    return open_info
