import re

short_months = {4, 6, 9, 11}
long_months = {1, 3, 5, 7, 8, 10, 12}

days_month = [-10000, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 10000]

# TODO možná bych mohl udělat datovou strukturu YearEntries, která bude mít v sobě pole YearEntry...
class YearEntry (object):
    def __init__(self, type_t="x", day=0, month=0, line_number=0, length=0):
        self.type = type_t
        self.day = day
        self.month = month
        self.line_number = line_number
        self.length = length
        self.pair: object = None
        self.same_place_occupant: object = None
        self.day_date_static = calculate_day_date(self.day, self.month)

    def day_date(self):
        self.day_date_static = calculate_day_date(self.day, self.month)
        return self.day_date_static

    def __str__(self):
        ret = self.type + " " + str(self.day) + "." + str(self.month) + "."
        gg = self.same_place_occupant
        while gg is not None:
            ret += gg.type + " " + str(gg.day) + "." + str(gg.month) + "."
            gg = gg.same_place_occupant
        return ret

    def __lt__(self, other):
        return self.day_date() < other.day_date()

    def __eq__(self, other):
        return self.day_date() == other.day_date()


def calculate_day_date(day, month):
    return day + days_month[month]


def decode_day_date (day_date):
    i = 0
    while day_date - days_month[i+1] > 0:
        i += 1
    return day_date - days_month[i], i


def date_is_valid(day, month):
    if not (0 < day < 32) and not (0 < month < 13):
        return False
    if month == 2 and not (0 < day < 29):
        return False
    if not (0 < day < 31) and month in short_months:
        return False
    elif not (0 < day < 32) and month in long_months:
        return False
    else:
        return True


class TripPlanner(object):
    # read input
    # create entries in array
    # compute optimal pairs
    def __init__(self):
        self.year_array = [YearEntry(day=decode_day_date(c)[0], month=decode_day_date(c)[1]) for c in range(1, 366)]
        # print(self.year_array)
        number_of_sentences = int(input())
        for i in range(number_of_sentences):
            self.extract_trip_from_sentence(input(), i+1)
        self.optimal_pairs = []
        self.find_optimal_pairs()
        self.print_optimal_pairs()

    def extract_trip_from_sentence(self, sentence, line_number):
        x = re.finditer("([^0-9]|\\A)[1-3]?[0-9]\\.([1][0-2]|[1-9])\\.", sentence)
        earliest_day = YearEntry(day=31, month=12)
        latest_day = YearEntry(day=1, month=1)
        date_found = False
        for i in x:
            date = i.group()
            day, month = filter(None, date.split("."))
            day = int(day)
            month = int(month)
            if date_is_valid(day, month):
                if day+days_month[month] > latest_day.day_date():
                    latest_day.day = day
                    latest_day.month = month
                if day+days_month[month] < earliest_day.day_date():
                    earliest_day.day = day
                    earliest_day.month = month
                date_found = True
        if date_found:
            if earliest_day.day_date() == latest_day.day_date():
                if self.year_array[latest_day.day_date()-1].type == "x":
                    self.year_array[latest_day.day_date()-1] = YearEntry("OneDay", latest_day.day, latest_day.month, line_number, latest_day.day_date()-earliest_day.day_date() + 1)
                    self.year_array[latest_day.day_date() - 1].pair = self.year_array[latest_day.day_date()-1]
                else:
                    current_entry = self.year_array[latest_day.day_date()-1]
                    while current_entry.same_place_occupant is not None:
                        current_entry = current_entry.same_place_occupant
                    current_entry.same_place_occupant = YearEntry("OneDay", latest_day.day, latest_day.month, line_number, latest_day.day_date()-earliest_day.day_date() + 1)
                    current_entry.same_place_occupant.pair = current_entry.same_place_occupant

            else:
                if self.year_array[earliest_day.day_date() - 1].type == "x":
                    self.year_array[earliest_day.day_date()-1] = YearEntry("Start", earliest_day.day, earliest_day.month, line_number, latest_day.day_date()-earliest_day.day_date() + 1)
                    self.year_array[earliest_day.day_date() - 1].pair = latest_day
                else:
                    current_entry = self.year_array[earliest_day.day_date() - 1]
                    while current_entry.same_place_occupant is not None:
                        current_entry = current_entry.same_place_occupant
                    current_entry.same_place_occupant = YearEntry("Start", earliest_day.day, earliest_day.month, line_number, latest_day.day_date()-earliest_day.day_date() + 1)
                    current_entry.same_place_occupant.pair = latest_day
                if self.year_array[latest_day.day_date() - 1].type == "x":
                    self.year_array[latest_day.day_date()-1] = YearEntry("End", latest_day.day, latest_day.month, line_number, latest_day.day_date()-earliest_day.day_date() + 1)
                    self.year_array[latest_day.day_date() - 1].pair = earliest_day
                else:
                    current_entry = self.year_array[latest_day.day_date() - 1]
                    while current_entry.same_place_occupant is not None:
                        current_entry = current_entry.same_place_occupant
                    current_entry.same_place_occupant = YearEntry("OneDay", latest_day.day, latest_day.month, line_number, latest_day.day_date() - earliest_day.day_date() + 1)
                    current_entry.same_place_occupant.pair = earliest_day

    def find_optimal_pairs(self):
        day_counter = 0
        last_ended = YearEntry()
        potentially_optimal_pairs = []
        most_time_spent = 0
        valid = False
        for i in self.year_array:
            print(i)
        for current_event in self.year_array:
            event = current_event
            while event is not None:
                if event.type != "x":
                    if (event.type == "Start" or event.type == "OneDay") and last_ended.type != "x" and valid:
                        if day_counter > 7:
                            if most_time_spent < last_ended.length + event.length:
                                most_time_spent = last_ended.length + event.length
                                potentially_optimal_pairs.clear()
                                potentially_optimal_pairs.append((last_ended, event))
                            elif most_time_spent == last_ended.length + event.length:
                                potentially_optimal_pairs.append((last_ended, event))
                        else:
                            valid = False
                    if event.type == "End" or event.type == "OneDay":

                        # TODO pot5ebuju, aby se v9c OneDay eventu v jednom dni vyhodnocovalo jako start, ale neprepisoval se mi last event, protoze potrebuji prvni entry, ktera ma odkazy na zbytek

                        last_ended = event
                        valid = True
                        day_counter = 0
                        break
                    day_counter = 0
                event = event.same_place_occupant
            day_counter += 1
        self.optimal_pairs = potentially_optimal_pairs

    def print_optimal_pairs(self):

        self.optimal_pairs.sort()
        first, second = self.optimal_pairs[0]
        print(first.length + second.length)
        for first, second in self.optimal_pairs:
            print(str(first.line_number) + " " + str(first.pair.day) + "." + str(first.pair.month) + ". " + str(first.day) + "." + str(first.month) + ". " +
                  str(second.line_number) + " " + str(second.day) + "." + str(second.month) + ". " + str(second.pair.day) + "." + str(second.pair.month) + ".")


if __name__ == '__main__':
    blob = TripPlanner()

    #print(blob.year_array)

    #for Day in blob.year_array:
    #    print(str(Day.day_date()) + " " + str(Day))
