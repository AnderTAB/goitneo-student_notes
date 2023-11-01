COMMANDS = [
    "hello",
    "close",
    "help",
    "add-contact (add-contact name address phone email birthday(DD.MM.YYYY))",
    "change-contact (change-contact name)",
    "delete-contact (delete-contact name)",
    "all-contacts",
    "find-contact (find-contact name or address or phone or email or birthday(DD.MM.YYYY))",
    "contacts-birthdays (contacts-birthdays days(int))",
    "find-notes (find-notes TITLE or text or date)",
    "add-note (add-note TITLE text date))",
    "delete-note (delete-note TITLE)",
    "change-note-title (change-note TITLE NEW_TITLE)",
    "change-note-title (change-note TITLE new_text)",
    "add-note-tags (add-note-tags *your tags*)",
    "delete-note-tag (delete-note TITLE Tag)",
    "change-note-tag (change-note-tag tag new_tag)",
    "find-note-tag (find-note-tag *your tags*)",
    "sort-note-tag (find-note-tag *your tags*)",
]


def _parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def _input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return e
        except TypeError as e:
            return e

    return inner


def close_bot():
    print("Good bye!")


def helloBot():
    print("How can I help you?")


def helpBot():
    for i in COMMANDS:
        print(f"{i}")


@_input_error
def add_contact(args):
    name, address, phone, email, birthday = args
    print(name, address, phone, email, birthday)


@_input_error
def change_contact(args):
    name, address, phone, email, birthday = args
    print(name, address, phone, email, birthday)


@_input_error
def delete_contact(args):
    name = args[0]
    print(name)


@_input_error
def find_contact(args):
    key = args[0]
    print(key)


@_input_error
def all_contacts():
    print("All Contacts")


@_input_error
def contacts_birthdays(args):
    days = args[0]
    print(days)


@_input_error
def find_notes(args):
    key = args[0]
    print(key)


@_input_error
def add_note(args):
    TITLE, text, date = args
    print(TITLE, text, date)


@_input_error
def delete_note(args):
    TITLE = args[0]

    print(TITLE)


@_input_error
def change_note_title(args):
    TITLE, NEW_TITLE = args

    print(TITLE, NEW_TITLE)


@_input_error
def change_note_text(args):
    TITLE, new_text = args

    print(TITLE, new_text)


@_input_error
def add_note_tags(args):
    TITLE, *tags = args

    print(TITLE, *tags)


@_input_error
def delete_note_tag(args):
    TITLE, tag = args

    print(TITLE, tag)


@_input_error
def change_note_tag(args):
    TITLE, tag, new_tag = args

    print(TITLE, tag, new_tag)


@_input_error
def find_note_tag(args):
    tags = args

    print(tags)


@_input_error
def sort_note_tag(args):
    tags = args

    print(tags)


def main():
    msg = "\n==============================\nWelcome to the assistant bot!\n\nI will help you with your student activity.\n==============================\n"
    print(msg)

    while True:
        user_input = input("Enter a command: ")
        command, *args = _parse_input(user_input)

        if command in ["good bye", "close", "exit"]:
            close_bot()
            break
        elif command == "hello":
            helloBot()
        elif command == "help":
            helpBot()
        elif command == "add-contact":
            add_contact(args)
        elif command == "delete-contact":
            delete_contact(args)
        elif command == "change-contact":
            change_contact(args)
        elif command == "find-contact":
            find_contact(args)
        elif command == "all-contacts":
            all_contacts()
        elif command == "find-notes":
            find_notes(args)
        elif command == "add-note":
            add_note(args)
        elif command == "delete-note":
            delete_note(args)
        elif command == "change-note-title":
            change_note_title(args)
        elif command == "change-note-text":
            change_note_text(args)
        elif command == "add-note-tags":
            add_note_tags(args)
        elif command == "delete-note-tag":
            delete_note_tag(args)
        elif command == "change-note-tag":
            change_note_tag(args)
        elif command == "find-note-tag":
            find_note_tag(args)
        elif command == "sort-note-tag":
            sort_note_tag(args)
        elif command == "contacts-birthdays":
            contacts_birthdays(args)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
