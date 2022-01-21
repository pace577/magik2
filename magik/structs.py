#!/usr/bin/env python3

from typing import Dict
from collections import UserDict
import time
import webbrowser

class Time:
    """Used to record time in a day. Contains 3 attributes: hours, minutes,
    seconds. Can compare two Time objects and find the time difference in
    seconds using mathematical operators."""

    def __init__(self, hours:int, minutes:int, seconds:int) -> None:
        if hours<0 or hours>23:
            raise ValueError("'hours' must lie between 0 and 23 (inclusive)")
        if minutes<0 or minutes>59:
            raise ValueError("'minutes' must lie between 0 and 59 (inclusive)")
        if seconds<0 or seconds>60:
            raise ValueError("'seconds' must lie between 0 and 60 (inclusive)")
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def __repr__(self) -> str:
        return f"<Time: {self.hours:02}:{self.minutes:02}:{self.seconds:02}>"

    def __add__(self, time_in_seconds):
        """Add current Time with given time in seconds, and return new Time."""
        time_in_seconds = self.to_seconds() + time_in_seconds
        time_in_seconds %= 86400 #number of seconds in a day
        hours = time_in_seconds // 3600
        time_in_seconds %= 3600
        minutes = time_in_seconds // 60
        time_in_seconds %= 60
        return Time(hours, minutes, time_in_seconds)

    def __sub__(self, other):
        out_sec = 0
        out_sec += (self.hours - other.hours)*3600 if (self.hours - other.hours) != 0 else 0
        out_sec += (self.minutes - other.minutes)*60 if (self.minutes - other.minutes) != 0 else 0
        out_sec += (self.seconds - other.seconds) if (self.seconds - other.seconds) != 0 else 0
        return out_sec

    def __eq__(self, other):
        if self.hours == other.hours and self.minutes == other.minutes and self.seconds == other.seconds:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.hours < other.hours:
            return True
        elif self.hours > other.hours:
            return False
        else:
            if self.minutes < other.minutes:
                return True
            elif self.minutes > other.minutes:
                return False
            else:
                if self.seconds < other.seconds:
                    return True
                else:
                    return False

    def __gt__(self, other):
        if self.hours > other.hours:
            return True
        elif self.hours < other.hours:
            return False
        else:
            if self.minutes > other.minutes:
                return True
            elif self.minutes < other.minutes:
                return False
            else:
                if self.seconds > other.seconds:
                    return True
                else:
                    return False

    def __le__(self, other):
        return not self.__gt__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __hash__(self) -> int:
        return self.to_seconds()

    def to_seconds(self):
        return self.hours*3600 + self.minutes*60 + self.seconds


class Slot:
    """Elementary building block of a Timetable. Has a starting time and ending
    time. Can store information of the next slot when used in a timetable. Has
    methods to find out if the slot is the current slot i.e. whether the current
    time lies between start and end times of slot."""

    slot_type = None
    next_slot = None
    def __init__(self, start_time: Time, end_time: Time):
        if start_time >= end_time:
            raise ValueError("start_time must be less than end_time")
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self) -> str:
        return f"<Slot: {self.slot_type}, {self.start_time}>"

    def get_current_time(self) -> Time:
        """Return current time as magik.structs.Time"""
        current_time_list = map(int, time.strftime("%H,%M,%S").split(','))
        return Time(*current_time_list)

    def is_current_slot(self):
        """Returns True if the current time is in the slot time interval, else
        returns False."""
        return self.is_current_slot_manual(self.get_current_time())

    def is_current_slot_manual(self, current_time: Time):
        """Gets current time from the user and check if slot is 'current
        slot'"""
        if current_time >= self.start_time and current_time < self.end_time:
            return True
        return False


class BaseClassSlot(Slot):
    """The building block of a student timetable. Contains method to check if
    user is early to next class."""
    def __init__(self, start_time: Time, end_time: Time):
        super().__init__(start_time, end_time)
        self.slot_type = "base_class"

    def __repr__(self) -> str:
        return f"<BaseClassSlot: {self.start_time}>"

    def find_next_class(self):
        """Find the next class in the dayschedule. This can return a non None
        value only when slots are connected in a linked list."""
        upcoming_slot = self.next_slot
        while upcoming_slot:
            if upcoming_slot.slot_type == "class":
                return upcoming_slot
            upcoming_slot = upcoming_slot.next_slot
        return None

    def find_next_non_empty_slot(self):
        """Find the next non empty slot in the dayschedule. This can return a
        non None value only when slots are connected in a linked list."""
        upcoming_slot = self.next_slot
        while upcoming_slot:
            if upcoming_slot.slot_type != "":
                return upcoming_slot
            upcoming_slot = upcoming_slot.next_slot
        return None

    def is_early_to_next_class(self, early_to_class_time):
        """Return True if difference between current time and ~start_time~ of
        next slot is less than ~early_to_class_time~. Return False if time until
        next class is longer than ~early_to_class_time~. Return None if next
        class doesn't exist."""
        next_class = self.find_next_class()
        if next_class:
            time_interval = next_class.start_time - self.get_current_time()
            if time_interval < early_to_class_time:
                return True
            return False
        return None

    def alert_early_class(self):
        print("You are early for next class. Should open next class link(n) or exit(e)?")

    def activate(self, config):
        """Tell the user that this is break time"""
        if not self.is_current_slot():
            print("This is not the current slot.")
        else:
            early_to_class_time = int(config['early_to_class_time'])
            if self.is_early_to_next_class(early_to_class_time):
                self.alert_early_class()
            else:
                self.activate_action(config)

    def activate_action(self, config):
        """Default action to be done in this slot. Overwrite this method when
        Subclassing BaseClassSlot to perform appropriate action."""
        pass


class ClassInfo(UserDict):
    """Contains class attributes such as lecture links, clsasroom links, and any
    other data that the user wishes to store"""
    def __init__(self, __dict, **kwargs) -> None:
        super().__init__(__dict, **kwargs)


class ClassSlot(BaseClassSlot):
    """Class Slot contains class start and end timings, along with class_id.
    class_id can be used to get more information about that particular class.
    Has methods to find out whether user is late to current ClassSlot or early
    to next ClassSlot."""
    def __init__(self, class_info: ClassInfo, start_time: Time, end_time: Time):
        super().__init__(start_time, end_time)
        self.slot_type = "class"
        self.class_info = class_info

    def __repr__(self) -> str:
        return f"<ClassSlot: {self.start_time}>"

    # def is_early_to_next_class(self, early_to_class_time):
    #     """Return True if difference between current time and ~start_time~ of
    #     next slot is less than ~early_to_class_time~."""
    #     if self.next_slot:
    #         time_interval = self.next_slot.start_time - self.get_current_time()
    #         if time_interval < early_to_class_time:
    #             return True
    #         return False
    #     return None

    def is_late_to_class(self, late_to_class_time):
        """Return True if difference between current time and ~start_time~ of
        current slot is greater than ~late_to_class_time~."""
        time_interval = self.get_current_time() - self.start_time
        return True if time_interval>late_to_class_time else False

    # def activate(self, config):
    #     """Performs appropriate actions depending upon time and user input"""
    #     if not self.is_current_slot():
    #         print("This is not the current slot.")
    #     else:
    #         early_to_class_time = int(config['early_to_class_time'])
    #         late_to_class_time = int(config['late_to_class_time'])
    #         openable_link_attribute = config['openable_link_attribute']
    #         is_early = self.is_early_to_next_class(early_to_class_time)
    #         is_late = self.is_late_to_class(late_to_class_time)
    #         if is_early:
    #             self.alert_early_class()
    #             #print("You are early for next class. Should open next class link(n) or exit(e)?")
    #         elif is_late and not is_early:
    #             print("You are late for class. Open current link(c), open next class link(n) or exit(e)?")
    #         elif not is_late:
    #             print("Opening current class link...")
    #             self.activate_action(openable_link_attribute)

    # def activate_action(self, openable_link_attribute):
    #     """Opens the link associated with openable_link_attribute. Use
    #     webbrowser to open appropriate link taken from self.class_info"""
    #     webbrowser.open(self.class_info[openable_link_attribute])

    def activate_action(self, config):
        """Opens the link associated with openable_link_attribute. Use
        webbrowser to open appropriate link taken from self.class_info"""
        late_to_class_time = int(config['late_to_class_time'])
        openable_link_attribute = config['openable_link_attribute']
        is_late = self.is_late_to_class(late_to_class_time)
        if is_late:
            print("You are late for class. Open current link(c), open next class link(n) or exit(e)?")
        elif not is_late:
            print("Opening current class link...")
            webbrowser.open(self.class_info[openable_link_attribute])


class BreakSlot(BaseClassSlot):
    """Use BreakSlot for break time slots"""
    def __init__(self, start_time: Time, end_time: Time):
        super().__init__(start_time, end_time)
        self.slot_type = "break"

    def __repr__(self) -> str:
        return f"<BreakSlot: {self.start_time}>"

    def activate_action(self, config):
        print("This is break time! Should open next slot(n) or exit(e)?")


class EmptySlot(BaseClassSlot):
    """Use EmptySlot for slots with no classes or breaks"""
    def __init__(self, start_time: Time, end_time: Time):
        super().__init__(start_time, end_time)
        self.slot_type = "break"

    def __repr__(self) -> str:
        return f"<EmptySlot: {self.start_time}>"

    def activate_action(self, config):
        print("Nothing in the current slot. Should open next slot(n) or exit(e)?")


class ZeroSlot(BaseClassSlot):
    """Use ZeroSlot at the beginning of the day, when none of the slots for the
    day started yet"""
    def __init__(self, start_time: Time, end_time: Time):
        super().__init__(start_time, end_time)
        self.slot_type = "EOD"

    def __repr__(self) -> str:
        return f"<EODSlot: {self.start_time}>"

    def activate_action(self, config):
        print("It's too early for your timetable to begin! Open next slot(n) or wait for some more time?")


class EODSlot(Slot):
    """Use EODSlot at End of Day, when all slots for the day are over"""
    def __init__(self, start_time: Time, end_time: Time):
        super().__init__(start_time, end_time)
        self.slot_type = "EOD"

    def __repr__(self) -> str:
        return f"<EODSlot: {self.start_time}>"

    def activate(self, config):
        """Tell the user that this is break time"""
        if not self.is_current_slot():
            print("This is not the current slot.")
        else:
            print("All slots for the day are over. Take some rest!")


class DaySchedule(UserDict):
    """Dictionary of Slots. Key: Time, Value: Slot."""
    # def __init__(self, dayschedule_dict: dict[time, slot]) -> None:
    #     self.dayschedule_dict = dayschedule_dict
    def __init__(self, dayschedule_dict: Dict[Time, Slot], **kwargs) -> None:
        super().__init__(dayschedule_dict, **kwargs)

    def get_current_slot(self):
        """Go through all the slots in the DaySchedule and return the current
        slot. Return None if none of the slots in the dayschedule are currently
        active. This means that some time in the day isn't covered by the slots
        in the DaySchedule."""
        for slot in self.data.values():
            if slot.is_current_slot():
                return slot
        return None


class TimeTable():
    """Dictionary of DaySchedules. Key: day(string), Value: DaySchedule"""
    def __init__(self) -> None:
        pass

    def from_dict(self):
        """Get timetable from dict"""
        pass
