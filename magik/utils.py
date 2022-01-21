#!/usr/bin/env python3

"""Contains all utility functions needed for magik"""

from pathlib import Path
from structs import ClassInfo
import configparser
import csv


config_file_name = "config.ini"
timetable_file_name = "timetable.csv"

def get_config_from_file():
    """Extracts configuration from the 'config.ini' file. Returns cfg_tuple which contains 3 terms:
    1. General configuration
    2. Subject list
    3. List of ClassInfo objects, each containing subject configuration"""
    config = configparser.ConfigParser()
    config_file_name = "config.ini"
    config.read(config_file_name)
    class_info_list = []
    for class_id, subject_name in config['Subjects'].items():
        class_info = {"subject_name": subject_name}
        class_info.update(dict(config[subject_name]))
        class_info_list.append(ClassInfo(class_id, class_info))

    cfg_tuple = (dict(config['General']), dict(config['Subjects']), class_info_list)
    return cfg_tuple

def generate_default_config(overwrite=False):
    """Generate a configuration file with defaults"""
    config = configparser.ConfigParser()
    sections = ["General", "Subjects", "Mathematics", "Computer Science"]
    subject_ids = get_ids_from_subject_names(sections[2:])
    subjects_dict = {subject_ids[idx]: sections[2+idx] for idx in range(len(sections[2:])) }
    subjects_info = {"live_lecture_link":"https://wiki.archlinux.org", "recorded_lecture_link":"https://duckduckgo.com"}

    # Write the configuration to ConfigParser object
    config[sections[0]] = {"class_slot_length": 60*60,
                           "early_to_class_time": 60*10,
                           "late_to_class_time": 60*20,
                           "openable_link_attribute":"live_lecture_link"}
    config[sections[1]] = subjects_dict
    for section in sections[2:]:
        config[section] = subjects_info

    config_file = Path(config_file_name)
    if config_file.is_file() and not overwrite:
        raise FileExistsError("Timetable already exists. Set overwrite=True to overwrite the existing timetable")
    else:
        with open(config_file, 'w') as configfile:
            config.write(configfile)

def generate_default_timetable(overwrite=False):
    """Generate a default timetable that can be later modified by the user."""
    default_times = ["09:00", "10:00", "11:00", "13:00", "14:00"]
    timetable_file = Path(timetable_file_name)
    if timetable_file.is_file() and not overwrite:
        raise FileExistsError("Timetable already exists. Set overwrite=True to overwrite the existing timetable")
    else:
        with open(timetable_file, 'w', newline='') as csvfile:
            fieldnames = ['Day'] + default_times
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'Day': 'Monday', '09:00': 'm', '10:00': 'cs', '11:00': '', '13:00': 'cs', '14:00': 'm'})
            writer.writerow({'Day': 'Tuesday', '09:00': 'm', '10:00': 'm', '11:00': 'cs', '13:00': 'm', '14:00': 'cs'})
            writer.writerow({'Day': 'Wednesday', '09:00': 'm', '10:00': '', '11:00': 'cs', '13:00': 'm', '14:00': 'm'})
            writer.writerow({'Day': 'Thursday', '09:00': 'm', '10:00': 'm', '11:00': 'cs', '13:00': 'm', '14:00': 'cs'})
            writer.writerow({'Day': 'Friday', '09:00': 'm', '10:00': '', '11:00': 'cs', '13:00': 'm', '14:00': 'm'})

def get_ids_from_subject_names(subject_names, delimiter=" "):
    """Generates id from first letter of the words in subject name. Assume words
    in subject names are space separated by default"""
    subject_ids = []
    for subject_name in subject_names:
        words = subject_name.split(delimiter)
        subject_id = ''.join([word[0] for word in words]).lower()
        if subject_id in subject_ids:
            base_subject_id = subject_id
            idx = 2
            subject_id += ("-"+str(idx))
            while subject_id in subject_ids:
                idx += 1
                subject_id = base_subject_id + "-" + str(idx)
        subject_ids.append(subject_id)
    return subject_ids

def get_timetable_from_csv():
    timetable_file = Path(timetable_file_name)
    timetable_dict = {}
    with open(timetable_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            day = row.pop('Day')
            timetable_dict[day] = row
    print(timetable_dict)
