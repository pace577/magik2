#!/usr/bin/env python3

import csv
from pathlib import Path
import configparser
from typing import Dict

from structs import Time, Slot, EmptySlot, BreakSlot, ClassSlot, EODSlot, ClassInfo
from utils import get_time_from_timestring, generate_config_file, generate_timetable
from defaults import (
    default_first_section_heading,
    # default_category_name,
    # default_category_name_plural,
    default_category_list,
    default_config_file_path,
    default_timetable_file_path,
    default_general_config,
    default_subjects_info,
    default_timetable_contents,
    default_timetable_fields
) #can import a configuration dict rather than a huge list of variables!
# Create a function to get update configuration using a dict. (I think we don't need such a thing... dict.update() might already do that.)

class Profile:
    def __init__(self,
                 config_file_path: Path = default_config_file_path,
                 timetable_file_path: Path = default_timetable_file_path,
                 ) -> None:
        """Constructor for a Profile object. Initialize configuration before
        calling any methods."""
        self.config_file_path = config_file_path
        self.timetable_file_path = timetable_file_path
        #self.initialize_config_from_files()

    def initialize_config_from_files(self):
        """Initialize the 'config', 'category_info' and 'timetable' attributes
        by reading the configuration file and the timetable csv file."""
        # Read default config first. Overwrite with user config as necessary
        self.config = default_general_config
        try:
            self.generate_default_profile_config()
            _, self.category_info = self.get_config_from_config_file()
        except FileExistsError:
            user_config, self.category_info = self.get_config_from_config_file()
            self.config.update(user_config)
        # timetable
        try:
            self.generate_default_timetable()
        except FileExistsError:
            pass
        self.timetable = self.get_timetable_from_timetable_csv()

    def generate_default_profile_config(self, overwrite=False):
        """Generate a default configuration file if it doesn't exist. Set
        overwrite=True to overwrite the existing timetable"""
        generate_config_file(self.config_file_path,
                             default_first_section_heading,
                             default_general_config,
                             default_category_list,
                             default_subjects_info,
                             overwrite=overwrite)

    def generate_default_timetable(self, overwrite=False):
        """Generate a default timetable csv if it doesn't exist. Set
        overwrite=True to overwrite the existing timetable"""
        generate_timetable(self.timetable_file_path,
                           default_timetable_fields,
                           default_timetable_contents,
                           overwrite=overwrite)

    def get_config_from_config_file(self):
        """Extracts configuration from the 'config.ini' file. Returns 2 dictionaries:
        1. General configuration dictionary
        2. Dictionary of class_id and ClassInfo objects (each containing subject configuration)
           as key-value pairs

        This function assumes that the sections in the config.ini file are organized as follows:
        Section 1: General Configuration (Heading: General)
        Section 2: Subject list (Heading: Subject)
        Section 3-end: Subject-wise information (Heading: <subject_name>)
        """
        config = configparser.ConfigParser()
        if self.config_file_path.is_file():
            config.read(self.config_file_path)
        else:
            raise FileNotFoundError("Configuration file doesn't exist. Create a configuration file or run Profile.generate_default_config() to create one.")

        category_info_dict = {}
        category_section_heading = self.config['category_heading']
        category = self.config['category_name']
        for category_id, category_name in config[category_section_heading].items(): # replace 'Subjects' with the category_name_plural configuration variable
            category_info = {category: category_name}
            category_info.update(dict(config[category_name]))
            category_info_dict[category_id] = ClassInfo(category_info)

        return dict(config[default_first_section_heading]), category_info_dict

    def get_timetable_from_timetable_csv(self):
        """Extracts timetable from the profile's timetable CSV."""
        timetable_dict = {}
        with open(self.timetable_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                day = row.pop('Day')
                timetable_dict[day] = self.get_dayschedule_from_dict(row)
        #print(timetable_dict)
        return timetable_dict

    def get_dayschedule_from_dict(self, dayschedule_dict: Dict[str, str]) -> Dict[Time, Slot]:
        """Return DaySchedule Object created using given dict as input."""
        out = {}
        # try:
        #     start_time = get_time_from_timestring(self.config['dayschedule_start_time'])
        # except KeyError as e:
        #     print(e)
        #     print("Set the 'dayschedule_start_time' variable in your config.ini file, with the HH:MM format.")
        if len(dayschedule_dict)>0:
            last_slot_length = 60*60 #can possibly set this as a configuration variable
            time_string_lst = list(map(get_time_from_timestring, dayschedule_dict.keys()))
            time_string_lst.append(time_string_lst[-1] + last_slot_length)

            for idx, slot in enumerate(dayschedule_dict.values()):
                # start_time = get_time_from_timestring(time_string_lst[idx])
                # end_time = get_time_from_timestring(time_string_lst[idx+1])
                start_time = time_string_lst[idx]
                end_time = time_string_lst[idx+1]
                out[start_time] = self.get_slot_from_slotstring(slot, start_time, end_time)
                if idx > 0:
                    previous_slot.next_slot = out[start_time]
                previous_slot = out[start_time]
            out[end_time] = EODSlot(end_time, Time(23,59,59))
            previous_slot.next_slot = out[end_time]
        return out

    def get_slot_from_slotstring(self, slot_string: str, start_time: Time, end_time: Time) -> Slot:
        if slot_string == '':
            return EmptySlot(start_time, end_time)
        elif slot_string == 'break':
            return BreakSlot(start_time, end_time)
        else:
            return ClassSlot(self.category_info[slot_string], start_time, end_time)
