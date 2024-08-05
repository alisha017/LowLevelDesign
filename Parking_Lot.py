import datetime
import uuid
from enum import Enum
from typing import List


class Size(Enum):
    COMPACT = 0
    NON_COMPACT = 1


class FuelType(Enum):
    ELECTRIC = 0
    GASOLINE = 1


class ParkingSpace:
    def __init__(self, size, special_needs, fuel_type, space_num, level):
        self.size = size
        self.special_needs = special_needs
        self.fuel_type = fuel_type
        self.space_num = space_num
        self.level = level
        self.occupied = False


class ParkingLevel:
    def __init__(self, level_num, no_of_spaces):
        self.level_num = level_num
        self.no_of_spaces = no_of_spaces
        self.parking_space_list:List[ParkingSpace] = []


class Ticket:
    def __init__(self, in_time):
        self.id = uuid.UUID()
        self.in_time = in_time


class ParkingLot:
    def __init__(self, levels, total_spaces):
        self.levels = levels
        self.total_spaces = total_spaces
        self.level_space = {}  # level: list of parking space
        self.unoccupied_spaces = self.total_spaces
        # self.unoccupied_spaces_at_each_level = {}  # level: unoccupied spaces count
        # self.total_space_at_each_level = {}  # level:total_spaces
        self.customers_tickets = {}

    @staticmethod
    def _calculate_charge(in_time, out_time):
        return datetime.timedelta(out_time, in_time) * 10

    def book_space(self):
        # generate_ticket - based on timetamp
        ticket_number = Ticket(datetime.datetime.now())
        self.unoccupied_spaces -= 1
        self.customers_tickets = {ticket_number.id: ticket_number}
        return ticket_number

    def release_space(self, ticket_num):
        release_time = datetime.datetime.now()
        to_release = self.customers_tickets[ticket_num]
        self.unoccupied_spaces += 1
        self.customers_tickets.pop(ticket_num)
        total_charge = self._calculate_charge(to_release.in_time, release_time)
        return total_charge





