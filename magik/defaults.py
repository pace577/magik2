#!/usr/bin/env python3

"""Defines all the default variables to be used across the program. These
variables can be overridden by user configuration."""

# default_config_sections = ["Configuration", "Subjects", "Mathematics", "Computer Science"]
# default_first_section_heading = "Configuration"
# default_category_name_plural = "Subjects"
# default_category_name = "Subject"
# default_category_list = ["Mathematics", "Computer Science"]

from pathlib import Path

default_config_path = Path("./")
default_config_file_path = default_config_path / 'config.ini'
default_timetable_file_path = default_config_path / 'timetable.csv'
default_first_section_heading = "Configuration"
default_general_config = {
    "category_heading": "Subjects",
    "category_name": "subject",
    # "category_list": ["Mathematics", "Computer Science"],
    "dayschedule_start_time": "09:00",
    "class_slot_length": 60*60,
    "early_to_class_time": 60*10,
    "late_to_class_time": 60*20,
    "openable_link_attribute":"live_lecture_link"
}
default_category_list = ["Mathematics", "Computer Science"]
default_subjects_info = {"live_lecture_link":"https://wiki.archlinux.org", "recorded_lecture_link":"https://duckduckgo.com"}

default_timetable_fields = ["Day", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00"]
default_timetable_contents = [
    {'Day': 'Monday', '09:00': 'm', '10:00': 'cs', '11:00': '', '12:00': 'break', '13:00': 'cs', '14:00': 'm'},
    {'Day': 'Tuesday', '09:00': 'm', '10:00': 'm', '11:00': 'cs', '12:00': 'break', '13:00': 'm', '14:00': 'cs'},
    {'Day': 'Wednesday', '09:00': 'm', '10:00': '', '11:00': 'cs', '12:00': 'break', '13:00': 'm', '14:00': 'm'},
    {'Day': 'Thursday', '09:00': 'm', '10:00': 'm', '11:00': 'cs', '12:00': 'break', '13:00': 'm', '14:00': 'cs'},
    {'Day': 'Friday', '09:00': 'm', '10:00': '', '11:00': 'cs', '12:00': 'break', '13:00': 'm', '14:00': 'm'},
]
