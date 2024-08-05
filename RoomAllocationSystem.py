# Design a room management systems which should allocated and deallocate rooms
# option to select room_type, room_facing
from enum import Enum
from typing import List, Deque, Dict
from collections import deque
import concurrent.futures
import threading


class RoomType(Enum):
    BASIC = 0
    DELUX_SUITE = 1
    MAHARAJA_SUITE = 2


class Room:
    def __init__(self, room_num:int, room_type:RoomType):
        self.room_num: int = room_num
        self.room_type: RoomType = room_type
        self.allocated = False


class Hotel:
    def __init__(self, total_rooms_count):
        self.total_rooms_count = total_rooms_count
        self.available_rooms: Dict[RoomType, Deque[Room]] = {room_type: deque() for room_type in RoomType}
        self.occupied_rooms: Dict[int, Room] = {}
        self.__add_rooms()
        self.lock = threading.Lock()

    def __define_room_type(self, room_num, room_type):
        new_room = Room(room_num, room_type)
        self.available_rooms[room_type].append(new_room)

    def __add_rooms(self):
        j = 0
        for room_type in RoomType:
            for i in range(0, 100):
                self.__define_room_type(i+j, room_type)
            j += 100

    def allocate_room(self, room_type: RoomType):
        if self.lock:
            try:
                rooms_available_in_room_type = self.available_rooms[room_type]
                if rooms_available_in_room_type:
                    room_available = rooms_available_in_room_type.popleft()
                    self.occupied_rooms[room_available.room_num] = room_available
                    return room_available.room_num, room_available.room_type.name
                else:
                    raise Exception(f"Room type : {room_type.name} not available ")
            except Exception as e:
                print(e)

    def deallocate_room(self, room_num):
        if self.lock:
            try:
                if room_num in self.occupied_rooms:
                    deallocated_room = self.occupied_rooms.pop(room_num)
                    self.available_rooms[deallocated_room.room_type].append(deallocated_room)
                    print(f"Room {room_num}, {deallocated_room.room_type.name} available again.")
                else:
                    raise Exception(f"Room number:{room_num} not occupied, cannot be deallocated")
            except Exception as e:
                print(e)


if __name__ == "__main__":
    taj_hotel = Hotel(15)


    def allocate_and_deallocate():
        with threading.Lock():
            list_rooms = []
            for _ in range(100):
                current_room = taj_hotel.allocate_room(RoomType.DELUX_SUITE)
                list_rooms.append(current_room)
                print(current_room)
            for _ in list_rooms:
                taj_hotel.deallocate_room(_[0])

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(allocate_and_deallocate) for _ in range(10)]
        # futures.extend([executor.submit(taj_hotel.deallocate_room, _) for _ in range(100, 200)])

        for future in concurrent.futures.as_completed(futures):
            future.result()
            print("**"*20)

    # print(taj_hotel.allocate_room(RoomType.MAHARAJA_SUITE))
    # print(taj_hotel.allocate_room(RoomType.MAHARAJA_SUITE))
    # print(taj_hotel.allocate_room(RoomType.MAHARAJA_SUITE))
    # print(taj_hotel.allocate_room(RoomType.MAHARAJA_SUITE))
    # print(taj_hotel.allocate_room(RoomType.MAHARAJA_SUITE))
    # print(taj_hotel.allocate_room(RoomType.MAHARAJA_SUITE))
    # taj_hotel.deallocate_room(21)
    # taj_hotel.deallocate_room(22)
    # taj_hotel.deallocate_room(23)
    # taj_hotel.deallocate_room(24)
    # taj_hotel.deallocate_room(25)
    # taj_hotel.deallocate_room(11)







