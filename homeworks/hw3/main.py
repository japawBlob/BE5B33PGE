import re

short_months = {4, 6, 9, 11}
long_months = {1, 3, 5, 7, 8, 10, 12}
month_names = ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"]


def date_is_valid(date):
    day, month = filter(None, date.split("."))
    day = int(day)
    month = int(month)
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


def find_exactly_one_month_in_sentence(sentence):
    counter = 0
    month_word = ""
    for word in re.split('[ .,?!]', sentence):
        if word in month_names:
            month_word = word
            counter += 1
            if counter > 1:
                return False
    if counter == 1:
        return month_word
    else:
        return False


def find_date_in_sentence(sentence, found_month):
    max_valid_date = -1
    if found_month == "February":
        max_valid_date = 28
    elif found_month in {"January", "March", "May", "July", "August", "October", "December"}:
        max_valid_date = 31
    else:
        max_valid_date = 30

    closest_number = -1
    closes_number_index = -1
    month_index = -1
    current_index = 0
    for word in re.split('[ ,]', sentence):
        if len(word) > 1 and word[-1] == '.':
            word = word.rstrip(word[-1])
        if word.isdigit() and (0 < int(word) <= max_valid_date):
            if month_index == -1:
                closest_number = int(word)
                closes_number_index = current_index
            else:
                if current_index-month_index < month_index-closes_number_index:
                    closest_number = int(word)
                break
        elif word == found_month:
            month_index = current_index
    return closest_number


def dm_date_to_string(dm_date):
    day, month, empty = dm_date.split(".")

    ret = (month_names[int(month)-1] + " " + day)
    return ret


class DateExtractor(object):
    def __init__(self):
        number_of_sentences = int(input())
        self.sentences = []
        for i in range(number_of_sentences):
            self.sentences.append(input())
        self.extractedDates = []

        blob = 1
        for i in self.sentences:
            ret = self.examine_sentence(i)
            if ret:
                print(str(blob) + ". " + ret)
            blob += 1

    def examine_sentence(self, sentence):
        # print(sentence)

        dm_date_found = self.check_for_dm_date(sentence)

        word = find_exactly_one_month_in_sentence(sentence)
        if word and not dm_date_found:
            # print(word)
            day = find_date_in_sentence(sentence, word)
            # print(day)

            if day != -1:
                # print("1 VALID")
                return str(word) + " " + str(day)
            else:
                # print("1 NOT VALID")
                return False
        elif word and dm_date_found:
            # print("2 NOT VALID")
            return False
        elif not word and dm_date_found:
            # print("2 VALID")
            # dm_date_to_string(dm_date_found)
            return dm_date_to_string(dm_date_found)
        else:
            # print("FOUND NOTHING")
            return False

    def check_for_dm_date(self, sentence):
        x = re.finditer("([^0-9]|\\A)[1-3]?[0-9]\\.([1][0-2]|[1-9])\\.", sentence)
        counter = 0
        found_date = ""
        for i in x:
            date = i.group()
            if date_is_valid(date):
                counter += 1
                if counter >= 2:
                    return False
                found_date = date
                # print(date)

                # print(date + " - is NOT valid")
        if 0 < counter < 2:
            # self.extractedDates.append(date)
            return found_date
        else:
            return False


if __name__ == '__main__':
    blob = DateExtractor()

    # blob.check_for_dm_date(blob.sentences[4])

    # blob.check_for_dm_date("31.2. 12.12. 31.4. 31.8. 32.1.")
