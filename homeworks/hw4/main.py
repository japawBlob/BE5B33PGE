import re

short_months = {4, 6, 9, 11}
long_months = {1, 3, 5, 7, 8, 10, 12}

days_month = [-10000, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 10000]


class YearEntry (object):
    def __init__(self, type_t="x", day=0, month=0, line_number=0, length=0):
        self.type = type_t
        self.day = day
        self.month = month
        self.line_number = line_number
        self.length = length
        self.pair = None
        self.day_date_static = calculate_day_date(self.day, self.month)

    def day_date(self):
        self.day_date_static = calculate_day_date(self.day, self.month)
        return self.day_date_static

    def __str__(self):
        ret = self.type + " " + str(self.day) + "." + str(self.month) + "."
        return ret

    def __lt__(self, other):
        if self.day_date() == other.day_date():
            return self.line_number < other.line_number
        return self.day_date() < other.day_date()

    def __eq__(self, other):
        return self.day_date() == other.day_date() and self.line_number == other.line_number


def calculate_day_date(day, month):
    return day + days_month[month]


def decode_day_date (day_date):
    i = 0
    while day_date - days_month[i+1] > 0:
        i += 1
    return day_date - days_month[i], i


def date_is_valid(day, month):
    if not (0 < day < 32) or not (0 < month < 13):
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
    def __init__(self):
        self.year_array = [[] for c in range(1, 366)]
        number_of_sentences = int(input())
        for i in range(number_of_sentences):
            self.extract_trip_from_sentence(input(), i+1)
        self.optimal_pairs = []
        self.find_optimal_pairs()
        # self.print_optimal_pairs()

    def extract_trip_from_sentence(self, sentence, line_number):

        sentence = sentence.replace(" ", "  ")
        # print("x  " + sentence + "  x")
        x = re.finditer("([ ]|\\A)[1-3]?[0-9]\\.([1][0-2]|[1-9])\\.([ ,\n]|\\Z)", sentence)
        earliest_day = YearEntry(day=31, month=12)
        latest_day = YearEntry(day=1, month=1)
        date_found = False
        for i in x:
            date = i.group().strip(" ,\n")
            # print(date)
            # for b in filter(None, date.split(".")):
            #     print("S--" + b + "--E")
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
                temp = YearEntry("OneDay", latest_day.day, latest_day.month, line_number, latest_day.day_date()-earliest_day.day_date() + 1)
                temp.pair = temp
                self.year_array[latest_day.day_date() - 1].append(temp)
            else:
                temp = YearEntry("Start", earliest_day.day, earliest_day.month, line_number, latest_day.day_date()-earliest_day.day_date() + 1)
                temp.pair = latest_day
                self.year_array[earliest_day.day_date() - 1].append(temp)
                temp = YearEntry("End", latest_day.day, latest_day.month, line_number, latest_day.day_date() - earliest_day.day_date() + 1)
                temp.pair = earliest_day
                self.year_array[latest_day.day_date() - 1].append(temp)

    def find_optimal_pairs(self):
        day_counter = 0
        will_be_last_ended = []
        last_ended = will_be_last_ended
        potentially_optimal_pairs = []
        most_time_spent = 0
        will_be_valid = False
        valid = will_be_valid
        change = False
        for events in self.year_array:
            if events:
                for event in events:
                    if event.type == "OneDay":
                        if last_ended and valid and day_counter > 7:
                            for current_last_ended in last_ended:
                                if most_time_spent < current_last_ended.length + event.length:
                                    most_time_spent = current_last_ended.length + event.length
                                    potentially_optimal_pairs.clear()
                                    potentially_optimal_pairs.append((current_last_ended, event))
                                elif most_time_spent == current_last_ended.length + event.length:
                                    potentially_optimal_pairs.append((current_last_ended, event))
                        will_be_last_ended.append(event)
                        will_be_valid = True
                        change = True
                    elif event.type == "Start":
                        if day_counter > 7 and last_ended and valid:
                            for current_last_ended in last_ended:
                                if most_time_spent < current_last_ended.length + event.length:
                                    most_time_spent = current_last_ended.length + event.length
                                    potentially_optimal_pairs.clear()
                                    potentially_optimal_pairs.append((current_last_ended, event))
                                elif most_time_spent == current_last_ended.length + event.length:
                                    potentially_optimal_pairs.append((current_last_ended, event))
                        else:
                            # will_be_last_ended = last_ended
                            change = True
                    elif event.type == "End":
                        will_be_last_ended.append(event)
                        will_be_valid = True
                        change = True
                day_counter = 0
            day_counter += 1
            if change:
                if will_be_last_ended:
                    last_ended = will_be_last_ended
                    will_be_last_ended = []
                valid = will_be_valid
                will_be_valid = False
                change = False
        self.optimal_pairs = potentially_optimal_pairs

    def print_optimal_pairs(self):
        self.optimal_pairs.sort()
        if self.optimal_pairs:
            first, second = self.optimal_pairs[0]
            print(first.length + second.length)
            for first, second in self.optimal_pairs:
                print(str(first.line_number) + " " + str(first.pair.day) + "." + str(first.pair.month) + ". " + str(first.day) + "." + str(first.month) + ". " +
                      str(second.line_number) + " " + str(second.day) + "." + str(second.month) + ". " + str(second.pair.day) + "." + str(second.pair.month) + ".")
        else:
            print("No matching pairs found")

    def get_optimal_pairs(self):
        self.optimal_pairs.sort()
        ret = ""
        if self.optimal_pairs:
            first, second = self.optimal_pairs[0]
            ret += str(first.length + second.length) + "\n"
            for first, second in self.optimal_pairs:
                ret += (str(first.line_number) + " " + str(first.pair.day) + "." + str(first.pair.month) + ". " + str(first.day) + "." + str(first.month) + ". " +
                      str(second.line_number) + " " + str(second.day) + "." + str(second.month) + ". " + str(second.pair.day) + "." + str(second.pair.month) + ".\n")
        else:
            ret += "No matching pairs found"
        return ret


if __name__ == '__main__':
    blob = TripPlanner()
    blob.print_optimal_pairs()


