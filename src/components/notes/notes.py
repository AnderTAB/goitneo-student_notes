from collections import UserDict
from datetime import datetime
from csv import DictReader, DictWriter
import re
import os


class Field:
    def __init__(self, text):
        self.text = text

    def __str__(self) -> str:
        return str(self.text)


class Title(Field):
    def __init__(self, title):
        self.text = title


class Tag(Field):
    def __init__(self, tag) -> None:
        self.text = tag


class Notation(Field):
    def __init__(self, title) -> None:
        self.text = title


class ID(Field):
    def __init__(self, id):
        self.text = str(id)


class Record:
    current_id = int(1)

    def __init__(self):
        self.title = None
        self.tag = []
        self.note = None
        self.date = datetime.now().strftime("%d.%m.%Y %H:%M")
        if Record.current_id not in notebook.get_id_list():
            self.id = ID(Record.current_id)
        else:
            Record.current_id = int(max(notebook.get_id_list())) + 1
            self.id = ID(Record.current_id)
        Record.current_id += 1

    def add_id(self, id):
        if id not in notebook.get_id_list():
            Record.current_id = id
            self.id = ID(Record.current_id)
        else:
            Record.current_id = int(max(notebook.get_id_list())) + 1
            self.id = ID(Record.current_id)
        Record.current_id += 1

    def add_title(self, title):
        self.title = Title(title)

    def add_tag(self, tags):
        if isinstance(tags, list):
            for t in tags:
                if t not in [t.text for t in self.tag]:
                    self.tag.append(Tag(t))
        elif isinstance(tags, str) and len(re.findall(r"#\w+", tags)) > 1:
            for t in re.findall(r"#\w+", tags):
                if t not in [t.text for t in self.tag]:
                    self.tag.append(Tag(t))
        else:
            if tags not in [t.text for t in self.tag]:
                self.tag.append(Tag(tags))

    def add_note(self, note):
        if len(note) <= 256:
            self.note = Notation(note)
        else:
            raise ValueError("Too mach symbols. 256 symbols are allowed")

    def edit_note(self, new_note):
        self.add_note(new_note)

    def edit_title(self, new_title):
        self.add_title(new_title)

    def edit_tag(self, old_tag, new_tag):
        for tag in self.tag:
            if tag.text == old_tag:
                tag.text = new_tag

    def del_tag(self, tag_to_delete):
        for tag in self.tag:
            if tag.text == tag_to_delete:
                self.tag.remove(tag)

    def create_record(self, text):
        self.add_title(self.find_title_in_text(text))
        self.add_tag(self.find_tags_in_text(text))
        self.add_note(self.find_note_in_text(text))

    def find_title_in_text(self, text):
        try:
            title = re.findall(r"(?<!#)\b[A-Z]+\b", text)
            return " ".join(title)
        except ValueError:
            print("No title found")
            return []

    def find_tags_in_text(self, text):
        try:
            tags = re.findall(r"#\w+", text)
            return tags
        except ValueError:
            print("No tags found")
            return []

    def find_note_in_text(self, text):
        try:
            pattern = re.compile(r"(?<!#)\b[A-Z]+\b")
            text = pattern.sub("", text)
            pattern = re.compile(r"#\w+")
            text = pattern.sub("", text)
            note = re.findall(r"\b\S.[^ ]*\b", text)
            return " ".join(note)
        except ValueError:
            print("No note found")
            return []

    def __str__(self) -> str:
        message = ("-" * 103) + "\n"
        if self.title:
            message += "|{:<15}|{:<85}|\n".format("Title", (self.title.text))
            message += ("-" * 103) + "\n"
        if self.note:
            message += "|{:<15}|{:<85}|\n".format("Notice", (self.note.text))
            message += ("-" * 103) + "\n"
        if self.tag:
            message += "|{:<15}|{:<85}|\n".format(
                "Tags", (" ".join(t.text for t in self.tag))
            )
        message += ("-" * 103) + "\n"
        message += "|{:<15}|{:<85}|\n".format("Date", (self.date))
        message += ("-" * 103) + "\n"
        message += "|{:<15}|{:<85}|\n".format("ID", (self.id.text))
        message += ("-" * 103) + "\n"
        return message


class NoteData(UserDict):
    def add_record(self, note):
        self.data[note.title.text] = note

    def get_id_list(self):
        dict_data = self.to_dict()
        id_list = [item["id"] for item in dict_data]
        return id_list

    def delete(self, note_name):
        if note_name in self.data:
            del self.data[note_name]
        else:
            return "No such note with name {note_name} found"

    def find_note(self, word):
        if len(word) >= 3:
            pattern = re.compile(word.lower())
            result = []
            for note in self.data:
                note_find = re.findall(pattern, self.data[note].note.text.lower())
                title_find = re.findall(pattern, self.data[note].title.text.lower())
                tag_find = re.findall(
                    pattern,
                    "".join(p.text.lower() for p in self.data[note].tag),
                )
                date_find = re.findall(pattern, self.data[note].date)
                if (
                    len(note_find) > 0
                    or len(title_find) > 0
                    or len(tag_find) > 0
                    or len(date_find) > 0
                ):
                    result.append(self.data[note])
                else:
                    continue
            if len(result) > 1:
                return result
            elif len(result) == 1:
                return result[0]
            else:
                return []
        else:
            raise ValueError("Search word schud have at least 3 characters")

    def find_note_by_tag(self, tag):
        result = []
        pattern = re.compile(tag)
        for note in self.data:
            tag_find = re.findall(
                pattern, " ".join(p.text.lower() for p in self.data[note].tag)
            )
            if len(tag_find) > 0:
                result.append(self.data[note])
            else:
                continue
        if len(result) > 1:
            return result
        elif len(result) == 1:
            return result[0]
        else:
            return []

    def find_note_by_date(self, date):
        result = []
        if re.match(r"\d{2}.\d{2}.\d{4}", date):
            pattern = re.compile(date)
            for note in self.data:
                if re.match(pattern, self.data[note].date):
                    result.append(self.data[note])
        else:
            return "Date schould be in format DD.MM.YYYY"
        if len(result) > 1:
            return result
        elif len(result) == 1:
            return result[0]
        else:
            return []

    def get_note_by_id(self, id):
        for note in self.data:
            if self.data[note].id.text == id:
                result = self.data[note]
                break
        return result if result is not None else None

    def sort_note_by_tag_amount(self, reverse=False):
        result = []
        result_dict = {}
        dict_data = self.to_dict()
        for d in dict_data:
            d["tag"] = d["tag"].split(",")
            result.append(d)
        sorted_list = sorted(result, key=lambda d: len(d["tag"]), reverse=reverse)
        for r in sorted_list:
            result_dict[r["title"]] = self.get_note_by_id(r["id"])
        return result_dict

    def to_dict(self, obj=None):
        result = []
        if obj is None:
            for rec in self.data:
                note_dict = {
                    "title": self.data[rec].title.text,
                    "tag": ", ".join(p.text for p in self.data[rec].tag),
                    "note": self.data[rec].note.text,
                    "date": self.data[rec].date,
                    "id": self.data[rec].id.text,
                }
                result.append(note_dict)
        elif isinstance(obj, list):
            for rec in obj:
                note_dict = {
                    "title": rec.title.text,
                    "tag": ", ".join(p.text for p in rec.tag),
                    "note": rec.note.text,
                    "date": rec.date,
                    "id": rec.id.text,
                }
                result.append(note_dict)
        else:
            note_dict = {
                "title": obj.title.text,
                "tag": ", ".join(p.text for p in obj.tag),
                "note": obj.note.text,
                "date": obj.date,
                "id": obj.id.text,
            }
            result.append(note_dict)
        return result

    def read_csv_file(self, file):
        # script_dir = "\\".join(os.path.dirname(__file__).split("\\")[:-3])
        file = os.path.abspath(f"src/db/notes/{file}")
        with open(file, "r") as f:
            dict_reader = DictReader(f, delimiter=";")
            note_data = list(dict_reader)

        for note in note_data:
            for key, value in note.items():
                if key == "title":
                    record = Record()
                    record.add_title(value)
                if key == "id":
                    record.add_id(int(value))
                elif key == "tag":
                    if len(value.split(",")) > 1:
                        for v in value.split(","):
                            record.add_tag(v.strip())
                    else:
                        record.add_tag(value)
                elif key == "note":
                    if note[key]:
                        record.add_note(value)
                    else:
                        continue
                elif key == "date":
                    if note[key]:
                        record.date = value
                    else:
                        continue
                else:
                    continue
                self.add_record(record)

    def write_csv_file(self, file):
        # script_dir = "\\".join(os.path.dirname(__file__).split("\\")[:-3])
        file = os.path.abspath(f"src/db/notes/{file}")
        field_names = ["title", "note", "tag", "date", "id"]
        users_list = self.to_dict()
        with open(file, "w") as csvfile:
            writer = DictWriter(csvfile, fieldnames=field_names, delimiter=";")
            writer.writeheader()
            writer.writerows(users_list)


# if __name__ == "__main__":
#     notebook = NoteData()  # create user dict object
#     notebook.read_csv_file("data.csv")  # read csv data
#     first_notation = Record()  # create record object
#     first_notation.add_title("SOME TASK")  # add title to created object
#     first_notation.add_note("Some text")  # add note to creted object
#     first_notation.add_tag("#Lab, #20")  # add tags to object
#     first_notation.add_tag("#Lab #20")  # check that tags are not duplicated
#     first_notation.add_tag("#paht")  # add single tag
#     notebook.add_record(first_notation)  # add object to user dict
#     #    print(first_notation)

#     # create another record object
#     first_notation = Record()

#     # To create a record automatically with the title in uppercase,
#     # tags with only '#' symbols, and the note containing the rest of the text
#     first_notation.create_record(
#         """
#                                  PROJECT SUBMISSION FOR HYDRODYNAMICS #PAKHT, #LABA, #20POINTS
#                                  It is necessary to complete a project on the topic "......"
#                                  Preliminary defense in the 4th building, room 201..."""
#     )
#     notebook.add_record(first_notation)  # add record to user dict

#     # To create a similar object with a different ID
#     some_notataion = Record()
#     some_notataion.create_record(
#         """
#                                  PROJECT SUBMISSION FOR HYDRODYNAMICS #PAKHT, #LABA, #20POINTS
#                                  It is necessary to complete a project on the topic "......"
#                                  Preliminary defense in the 4th building, room 201..."""
#     )
#     notebook.add_record(some_notataion)

#     second_notation = Record()
#     second_notation.create_record(
#         """LIST TO DO #koliu, #goit not so important 5463899"""
#     )
#     notebook.add_record(second_notation)

#     # To edit a record, the best and safest way is to find the record by its ID.
#     # If it is found, then it can be edited.
#     id_find = notebook.get_note_by_id("2")  #
#     print(id_find)
#     id_find.edit_note("something")
#     print(id_find)
#     id_find.edit_title("nothing")
#     print(id_find)
#     id_find.edit_tag("#window", "#ok")
#     print(id_find)

#     # Of course, it could be edited in another way by using a different search options,
#     # but you must be careful since such a search method may return a list.
#     print(notebook.find_note("Almost election."))
#     notebook.delete("Almost election.")  # delete the record
#     print(notebook.find_note("Almost election."))
#     second_find = notebook.find_note("200")
#     for r in second_find:
#         print(str(r))

#     # returns all data as dict
#     dict_result = notebook.to_dict()
#     print(dict_result)

#     # it returns a dictionary created from the object.
#     dict_result = notebook.to_dict(second_find)
#     print(dict_result)

#     print(notebook.get_id_list())

#     print("Hier ist the full list: \n")
#     for name, record in notebook.data.items():
#         print(str(record) + "\n")

# #    notebook.write_csv_file("fake_note_1.csv")
