#!/usr/bin/env python3

"""Contains all utility functions needed for magik"""

from pathlib import Path
import configparser
import csv
from typing import Dict
from structs import Time, Slot

timetable_file_name = "timetable.csv"

def generate_timetable(timetable_file_path, timetable_fields, timetable_contents, overwrite=False):
    """Generate a default timetable that can be later modified by the user."""
    timetable_file = Path(timetable_file_path)
    # default_times = ["09:00", "10:00", "11:00", "13:00", "14:00"]
    if timetable_file.is_file() and not overwrite:
        raise FileExistsError("Timetable already exists. Set overwrite=True to overwrite the existing timetable")
    else:
        with open(timetable_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=timetable_fields)
            writer.writeheader()
            for item in timetable_contents:
                writer.writerow(item)

def generate_config_file(config_file_path,
                         first_section_heading,
                         general_config,
                         category_list,
                         category_info,
                         overwrite=False):
    """ Generate a configuration file with given parameters
    There are 2 mandatory sections, and any number of optional sections thereafter.
    Mandatory sections:
    1. Configuration: Contains all the general configuration
    2. Categories: List of all optional categories. For example, if categories
    are subjects, then we have a list of all subjects in this section
    3-end. <category_name>: Contains information about the category. For
    example, if the category is a subject, then it contains all information about
    that subject.
    """

    config_file = Path(config_file_path)
    if config_file.is_file() and not overwrite:
        raise FileExistsError("Timetable already exists. Set overwrite=True to overwrite the existing timetable")
    else:
        config = configparser.ConfigParser()
        category_heading = general_config['category_heading']
        sections = [first_section_heading, category_heading] + category_list
        category_ids = get_ids_from_category_names(category_list)
        category_dict = {category_ids[idx]: category_list[idx] for idx in range(len(category_list)) }

        # Write the configuration to ConfigParser object
        config[sections[0]] = general_config
        config[sections[1]] = category_dict
        for category in sections[2:]:
            config[category] = category_info
        with open(config_file, 'w') as configfile:
            config.write(configfile)

def get_ids_from_category_names(category_names, delimiter=" "):
    """Generates id from first letter of the words in section (subject) name. Assume words
    in section names are space separated by default"""
    category_ids = []
    for category_name in category_names:
        words = category_name.split(delimiter)
        category_id = ''.join([word[0] for word in words]).lower()
        if category_id in category_ids:
            base_category_id = category_id
            idx = 2
            category_id += ("-"+str(idx))
            while category_id in category_ids:
                idx += 1
                category_id = base_category_id + "-" + str(idx)
        category_ids.append(category_id)
    return category_ids

def get_timetable_from_csv():
    timetable_file = Path(timetable_file_name)
    timetable_dict = {}
    with open(timetable_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            day = row.pop('day')
            timetable_dict[day] = row
    print(timetable_dict)

def get_dayschedule_from_dict(dayschedule_dict: Dict[str, str]) -> Dict[Time, Slot]:
    """Return DaySchedule Object created using given dict as input."""
    out = {}
    for time, slot in dayschedule_dict.items():
        out[get_time_from_timestring(time)] = get_slot_from_slotstring(slot)

def get_time_from_timestring(time_string: str, delimiter: str = ":") -> Time:
    """Returns Time object from time string. time_string is of the format 'HH:MM'"""
    hrs, mins = map(int, time_string.split(delimiter))
    return Time(hrs, mins, 0)
