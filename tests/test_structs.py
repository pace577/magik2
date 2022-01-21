#!/usr/bin/env python3

import pytest
from magik.structs import Time, Slot


a_hr = Time(10,0,30)
b_hr = Time(9,0,30)
a_sec = Time(9,0,50)
b_sec = Time(9,0,30)
a_zero = Time(0,0,0)
b_zero = Time(0,0,0)
a_eq = Time(14,20,19)
b_eq = Time(14,20,19)

class TestTime:
    def test_time_init_1(self):
        with pytest.raises(ValueError):
            Time(24,0,0)

    def test_time_init_2(self):
        with pytest.raises(ValueError):
            Time(0,70,0)

    def test_time_init_3(self):
        with pytest.raises(ValueError):
            Time(0,0,100)

    def test_time_sub_1(self):
        assert (a_sec - b_sec) == 20

    def test_time_sub_2(self):
        assert (b_hr - a_hr) == -3600

    def test_time_sub_3(self):
        assert (a_zero - b_zero) == 0

    def test_time_lt(self):
        assert (a_eq < b_eq) == False


tmp_slot = Slot(Time(9,0,30), Time(10,0,30))
class TestSlot:
    def test_slot_init_1(self):
        with pytest.raises(ValueError):
            Slot(Time(12,30,0), Time(12,30,0))

    def test_slot_init_2(self):
        with pytest.raises(ValueError):
            Slot(Time(12,30,0), Time(12,29,59))

    def test_current_time_manual_1(self):
        assert tmp_slot.is_current_slot_manual(Time(9,30,0)) == True
