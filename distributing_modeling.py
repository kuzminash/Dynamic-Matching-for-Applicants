from random import *
from typing import Final

APPLICANTS = 8000
PROGRAMS: Final = 100
PLACES: Final = 60
PROGRAMSINLIST: Final = 10


class Applicant:
    def __init__(self, position, programs_in_order):
        self.position = position
        self._programs_in_order = programs_in_order
        self._offers = []

    def get_offer(self, program):
        self._offers.append(program)

    def decline_offers(self):
        if len(self._offers) <= 1:
            return []
        self._offers.sort(key=lambda program: self._programs_in_order.index(program), reverse=True)
        to_decline = self._offers[1:]
        self._offers = self._offers[:1]
        return to_decline

    def has_offer(self):
        return len(self._offers) != 0


class Program:
    def __init__(self, position, places):
        self.position = position
        self._applicants = []
        self._agreed = set()
        self._pointer = 0
        self._available_places = places

    def new_applicant(self, applicant):
        self._applicants.append(applicant)

    def send_offers(self):
        pointer = self._pointer
        available_places = self._available_places
        applicants_who_get_offer = []
        for _ in range(pointer, pointer + available_places):
            if self._pointer == len(self._applicants): break
            applicants_who_get_offer.append(self._applicants[self._pointer])
            self._agreed.add(self._applicants[self._pointer])
            self._available_places += 1
            self._pointer += 1
        return applicants_who_get_offer

    def get_reject(self, applicant):
        self._agreed.remove(applicant)
        self._available_places -= 1

    def can_send_anyone(self):
        return self._available_places != 0 and self._pointer != len(self._applicants)


def main_wave(applicants, programs):
    days = 0
    while True:
        days += 1
        has_programs = False
        for program in programs:
            if program.can_send_anyone():
                has_programs = True
                new_offers = program.send_offers()
                for applicant in new_offers:
                    applicant.get_offer(program)

        if not has_programs: break

        for applicant in applicants:
            decline_offers = applicant.decline_offers()
            for decline in decline_offers:
                decline.get_reject(applicant)
    return days

def cycle():
    applicants = []
    programs = []
    for i in range(PROGRAMS):
        programs.append(Program(i, PLACES))

    for i in range(APPLICANTS):
        programs_in_order = sample(programs, k=PROGRAMSINLIST)
        applicants.append(Applicant(i, programs_in_order))
        for program in programs_in_order:
            program.new_applicant(applicants[-1])

    days = main_wave(applicants, programs)
    return days


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    days = []
    APPLICANTS = 1000
    while APPLICANTS <= 16000:
        for i in range(1000):
            days.append(cycle())
        print('APPLICANTS ' + str(APPLICANTS))
        print(f'Min {min(days)}')
        print(f'Max {max(days)}')
        print(f'Mean {sum(days) / len(days)}')
        print()
        APPLICANTS += 1000

