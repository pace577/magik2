#!/usr/bin/env python3

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


class Slot:
    """Elementary building block of a Time table. Has a starting time and ending
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

    def __get_current_time(self) -> Time:
        """Return current time as magik.structs.Time"""
        current_time_list = map(int, time.strftime("%H,%M,%S").split(','))
        return Time(*current_time_list)

    def is_current_slot(self):
        """Returns True if the current time is in the slot time interval, else
        returns False."""
        return self.is_current_slot_manual(self.__get_current_time())

    def is_current_slot_manual(self, current_time: Time):
        """Gets current time from the user and check if slot is 'current
        slot'"""
        if current_time > self.start_time and current_time < self.end_time:
            return True
        return False


class ClassInfo(UserDict):
    """Contains class attributes such as lecture links, clsasroom links, and any
    other data that the user wishes to store"""
    def __init__(self, class_id: str, __dict, **kwargs) -> None:
        self.class_id = class_id
        super().__init__(__dict, **kwargs)


class ClassSlot(Slot):
    """Class Slot contains class start and end timings, along with class_id.
    class_id can be used to get more information about that particular class.
    Has methods to find out whether user is late to current ClassSlot or early
    to next ClassSlot."""
    def __init__(self, class_info: ClassInfo, start_time: Time, end_time: Time):
        super().__init__(start_time, end_time)
        self.slot_type = "class"
        self.class_info = class_info

    def is_early_to_next_class(self, early_to_class_time):
        """Return True if difference between current time and ~start_time~ of
        next slot is less than ~early_to_class_time~."""
        if self.next_slot:
            time_interval = self.next_slot.start_time - self.__get_current_time()
            if time_interval < early_to_class_time:
                return True
            return False
        return None

    def is_late_to_class(self, late_to_class_time):
        """Return True if difference between current time and ~start_time~ of
        current slot is greater than ~late_to_class_time~."""
        time_interval = self.__get_current_time() - self.start_time
        return True if time_interval>late_to_class_time else False

    def activate(self, early_to_class_time, late_to_class_time, openable_link_attribute):
        """Performs appropriate actions depending upon time and user input"""
        if not self.is_current_slot():
            print("This is not the current slot.")
        else:
            is_early = self.is_early_to_next_class(early_to_class_time)
            is_late = self.is_late_to_class(late_to_class_time)
            if is_early:
                print("You are early for next class. Should open next class link(n) or exit(e)?")
            elif is_late and not is_early:
                print("You are late for class. Open current link(c), open next class link(n) or exit(e)?")
            elif not is_late:
                print("Opening current class link...")
                self.__activate_action(openable_link_attribute)

    def __activate_action(self, openable_link_attribute):
        """Opens the link associated with openable_link_attribute. Use
        webbrowser to open appropriate link taken from self.class_info"""
        webbrowser.open(self.class_info[openable_link_attribute])


class BreakSlot(Slot):
    """Use BreakSlot for break time slots"""
    def __init__(self, start_time: Time, end_time: Time):
        super().__init__(start_time, end_time)
        self.slot_type = "break"

    def activate(self):
        """Tell the user that this is break time"""
        if not self.is_current_slot():
            print("This is not the current slot.")
        else:
            print("This is break time! Should open next slot(n) or exit(e)?")


class EmptySlot(Slot):
    """Use EmptySlot for slots with no classes or breaks"""
    def __init__(self, start_time: Time, end_time: Time):
        super().__init__(start_time, end_time)
        self.slot_type = "break"

    def activate(self):
        """Tell the user that this is break time"""
        if not self.is_current_slot():
            print("This is not the current slot.")
        else:
            print("Nothing in the current slot. Should open next slot(n) or exit(e)?")


class EODSlot(Slot):
    """Use EODSlot at End of Day, when all slots for the day are over"""
    def __init__(self, start_time: Time, end_time: Time):
        super().__init__(start_time, end_time)
        self.slot_type = "EOD"

    def activate(self):
        """Tell the user that this is break time"""
        if not self.is_current_slot():
            print("This is not the current slot.")
        else:
            print("All slots for the day are over. Take some rest!")

class DaySchedule():
    """Dictionary of Slots. Key: Time, Value: Slot."""
    pass

class TimeTable():
    """Dictionary of DaySchedules. Key: day(string), Value: DaySchedule"""
    def __init__(self) -> None:
        pass

    def from_dict():
        """Get timetable from dict"""
        pass
