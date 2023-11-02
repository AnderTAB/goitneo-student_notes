from collections import UserDict
from datetime import datetime, timedelta
import json
import os.path

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    def __hash__(self):
        return hash(self.value)


class Phone(Field):
    def __init__(self, value):
        if value.isdigit() and len(value) == 10:
            super().__init__(value)
        else:
            raise ValueError("Invalid phone number")


class Birthday(Field):
    DATE_FORMAT = "%d.%m.%Y"

    def __init__(self, value):
        date_obj = datetime.strptime(value, self.DATE_FORMAT)
        super().__init__(date_obj.date())

    def __lt__(self, other):
        if isinstance(other, Birthday):
            return self.value < other.value

    def __gt__(self, other):
        if isinstance(other, Birthday):
            return self.value > other.value


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phone = ""
        self.birthday = "None"

    def add_phone(self, value):
        self.phone = Phone(value)

    def edit_phone(self, new_phone):
        self.phone = new_phone
        return f"Phone number updated to {new_phone}"

    def __str__(self):
        return (
            f"Contact name: {self.name}, phone: {self.phone}, birthday: {self.birthday}"
        )


class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def save_to_file(self, filename):
        filename = 'bd.json'

        if os.path.exists(filename) == False:
            with open(filename,'w') as file: 
                bd = {}
                json.dump(bd, file)
        
        with open(filename) as file:
            data = json.load(file)
            record = {}
            for el in self.data:
                res = str(self.data[el]).replace(',', '').split()                            
                data[res[2]] = [
                        {
                        "address": '',
                        "phone": res[4],
                        "email": '',
                        "birthdate": res[6]
                        }
                    ]   
                           
        with open(filename, "w") as file:
            json.dump(data, file,indent=2)

    def read_from_file(self, filename):
        try:
            with open(filename, "r") as file:              
                data = json.load(file)
                for key, value in data.items():                   
                    self.name = key
                    self.phone = value[0]['phone']
                    if value[0]['birthdate'] != 'None':
                        date = str(value[0]['birthdate']).split('-')
                        birthday = f'{date[2]}.{date[1]}.{date[0]}'
                    else:
                        birthday = None
                    record = Record(key)
                    record.add_phone(self.phone)
                    if birthday != None:
                        record.birthday = Birthday(birthday)
                    self.data[key] = record

        except FileNotFoundError:
            self.data = {}

    def add_record(self, record):
        self.data[record.name] = record

    def find(self, name):
        res = self.data.get(name)
        if res:
            return res
        else:
            raise ValueError("Contact not found")

    def add_birthday(self, name, birthday):
        try:
            contact = self.find(name)
        except ValueError:
            print("Contact not found")
        else:
            contact.birthday = Birthday(birthday)
            print("Birthday added.")

    def show_birthday(self, name):
        for i in self.data:
            if i == name:
                return self.data[i].birthday
            else:
                raise ValueError("Contact not found")

    def birthdays(self,diff):
        birthday_dict = {}
        for user in sorted(self.data.values(), key=lambda x: x.birthday):
            current_date = datetime.now().date()
            next_year = current_date.year + 1
            birthday = user.birthday
            if birthday == "None":
                continue
            birthday = birthday.value
            birthday_this_year = birthday.replace(year=current_date.year)
            if birthday_this_year < current_date:
                birthday_this_year = birthday.replace(year=next_year)

            delta_days = current_date + timedelta(days = int(diff[0]))

            if birthday_this_year == delta_days:
                weekday = birthday_this_year.strftime("%A")
                if weekday in birthday_dict:
                    birthday_dict[weekday] += [user.name]
                else:
                    birthday_dict[weekday] = [user.name]

        res = "\nAll Birthdays:\n"
        for day, names in birthday_dict.items():
            res += f"{day}: {', '.join(map(str, names))}\n"
        return res
