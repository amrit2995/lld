# import time

# class Elevator:
#     def __init__(self, floors):
#         self.floors = [False for _ in range(floors+1)]
#         self.curr_floor = 0
#         self.max_floor = 0
#         self.min_floor = 0
#         self.dir = 0
#         self.exit = False

#     def enter_destination(self, floor):

#         if floor not in range(0,len(self.floors)+1):
#             print(f"Ignore invalid destination floor: {floor}")

#         self.floors[floor] = True
#         self.max_floor = max(self.max_floor, floor)
#         self.min_floor = min(self.min_floor, floor)

#     def is_destination(self):
#         if self.floors[self.curr_floor]:
#             self.floors[self.curr_floor] = False
#             print(f"Passengers of {self.curr_floor} can exit")

#     def next_floor(self):
#         time.sleep(1)
#         self.curr_floor += self.dir
#         print(f"{self.curr_floor} floor")

#         if self.dir != 0:
#             self.is_destination()

#     def set_direction(self):
#         if self.dir == 0:
#             if self.max_floor > self.curr_floor:
#                 self.dir = 1
#             elif self.min_floor < self.curr_floor:
#                 self.dir = -1
#         elif self.dir  == 1:
#             if self.curr_floor >= self.max_floor:
#                 self.max_floor = 0
#                 if self.curr_floor > self.min_floor:
#                     self.dir = -1
#                 else:
#                     self.dir = 0
#         elif self.dir == -1:
#             if self.curr_floor <= self.min_floor:
#                 self.min_floor = len(self.floors)
#                 if self.curr_floor < self.max_floor:
#                     self.dir = 1
#                 else:
#                     self.dir = 0

#     def exit(self):
#         self.exit = True

#     def start(self):
#         while True:
#             self.set_direction()
#             self.next_floor()
#             if self.exit:
#                 print("Elevator closed")
#                 break


# e = Elevator(25)
# e.start()
# time.sleep(1)
# e.enter_destination(4)
# time.sleep(3)
# e.enter_destination(10)
# e.enter_destination(2)
# time.sleep(6)
# e.enter_destination(11)
# e.exit()

import asyncio

class Elevator:
    def __init__(self, floors):
        self.floors = [False for _ in range(floors+1)]
        self.curr_floor = 0
        self.max_floor = 0
        self.min_floor = len(self.floors)
        self.dir = 0
        self.exit = False
        self.lock = asyncio.Lock()  # Use asyncio.Lock for synchronization

    async def enter_destination(self, floor):
        async with self.lock:
            if self.exit:
                print(f"No new entry since lift closed")
                return
            if floor not in range(0, len(self.floors) + 1):
                print(f"Ignore invalid destination floor: {floor}")
                return
            print(f"Entry for {floor} floor added")
            self.floors[floor] = True

            if floor > self.curr_floor:
                self.max_floor = max(self.max_floor, floor)
            if floor < self.curr_floor:
                self.min_floor = min(self.min_floor, floor)

    def is_destination(self):
        if self.floors[self.curr_floor]:
            self.floors[self.curr_floor] = False
            print(f"Passengers of {self.curr_floor} can exit")

    async def next_floor(self):
        async with self.lock:
            await asyncio.sleep(1)
            self.curr_floor += self.dir
            print(f"{self.curr_floor} floor")
            # print(self.min_floor,self.curr_floor, self.max_floor, self.dir)
            self.is_destination()

    async def set_direction(self):
        async with self.lock:
            if self.dir == 0:
                if self.max_floor > self.curr_floor:
                    self.dir = 1
                elif self.min_floor < self.curr_floor:
                    self.dir = -1
            elif self.dir == 1:
                if self.curr_floor >= self.max_floor:
                    self.max_floor = 0
                    if self.curr_floor > self.min_floor:
                        self.dir = -1
                    else:
                        self.dir = 0
            elif self.dir == -1:
                if self.curr_floor <= self.min_floor:
                    self.min_floor = len(self.floors)
                    if self.curr_floor < self.max_floor:
                        self.dir = 1
                    else:
                        self.dir = 0

    async def set_exit(self):
        async with self.lock:
            self.exit = True

    async def start(self):
        while True:
            await self.set_direction()
            await self.next_floor()
            if self.exit and not self.min_floor < self.curr_floor and not self.curr_floor < self.max_floor:
                break

async def main():
    e = Elevator(25)
    elevator_task = asyncio.create_task(e.start())

    await asyncio.sleep(1)
    await e.enter_destination(4)
    await asyncio.sleep(15)
    await e.enter_destination(10)
    await e.enter_destination(2)
    await asyncio.sleep(6)
    await e.enter_destination(11)

    # await e.set_exit()
    await elevator_task

if __name__ == "__main__":
    asyncio.run(main())
