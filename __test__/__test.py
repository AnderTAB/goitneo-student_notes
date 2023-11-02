import subprocess
import os


# Список команд для выполнения
commands = [
    "hello",
    "help",
    "add_contact Dave1 Baker.str 1234567890 emaildada@gmail.com 3.11.1996"
    "add_contact Dave Baker.str 1234567890 emaildada@gmail.com 12-6-1996",
    "add_contact Dave Baker.str 1234567890 emaildada&gmail.com 12.6.1996",
    "add_contact Dave Baker.str 123 emaildada@gmail.com 12-6-1996",
    "add_contact Dave",
    "add_contact Dave Baker.str",
    "add_contact Dave Baker.str 1234567890",
    "add_contact Dave Baker.str 1234567890 emaildada@gmail.com",
    "add_contact Dave2 Baker.str 1234567890 emaildada@gmail.com 4.11.1996",
    "add_contact Dave3 Baker.str 1234567890 emaildada@gmail.com 5.6.1996",
    "add_contact Dave4 Baker.str 1234567890 emaildada@gmail.com 5.6.1996",
    "add_contact Dave5 Baker.str 1234567890 emaildada@gmail.com 6.6.1996",
    "add_contact Dave6 Baker.str 1234567890 emaildada@gmail.com 7.6.1996",
    "add_contact Dave7 Baker.str 1234567890 emaildada@gmail.com 8.6.1996",
    "add_contact Dave8 Baker.str 1234567890 emaildada@gmail.com 8.6.1996",
    "add_contact Dave9 Baker.str 1234567890 emaildada@gmail.com 8.6.1996",
    "add_contact Dave10 Baker.str 1234567890 emaildada@gmail.com 9.6.1996",
    "add_contact Dave11 Baker.str 1234567890 emaildada@gmail.com 10.6.1996",
    "change_contact Dave4 Baker.str 1234567890 emaildada@gmail.com 6.6.1996",
    "change_contact Dave4 Baker.str 1234567890 emaildada@gmail.com 5-6-1996"
    "change_contact Dave4 Baker.str 1234567890 emaildada@gmail.com",
    "change_contact Dave4 Baker.str 1234567890",
    "change_contact Dave4 Baker.str",
    "change_contact Dave4",
    "change_contact Dave4 Baker.str 1234567890 emailNEW@gmail.com 6.6.1996"
    "change_contact Dave4 Baker.str 1234567890 emailBAD&gmail.com 6.6.1996"
    "change_contact Dave4 Baker.str 0987654321 emaildada@gmail.com 6.6.1996"
    "change_contact Dave4 Baker.str 123 emaildada@gmail.com 6.6.1996"
    "change_contact Carl Baker.str 1234567890 emaildada@gmail.com 6.6.1996"
    "delete_contact Dave9",
    "all_contacts",
    "find_contact Dave4",
    "find_contact Dave9",
    "find_contact Baker.str",
    "find_contact Bimg.str",
    "find_contact 1234567890",
    "find_contact 0987654321",
    "find_contact emaildada@gmail.com",
    "find_contact nothing@gmail.com",
    "find_contact 10.6.1996",
    "find_contact 15.6.1996",
    "find_contact 15-6-1996",
    "contacts_birthdays 1",
    "contacts_birthdays 5",
    "contacts_birthdays 7",
    "add_note IT IT its cool",
    "add_note IT2 IT its cool #IT2",
    "add_note TITLE",
    "add_note text",
    "add_note TEMP",
    "find_notes IT",
    "find_notes QC",
    "find_notes IT",
    "find_notes its cool",
    "find_notes IT",
    "find_notes its bad",
    "find_notes 03.11.2023",
    "find_notes 04.08.2022",
    "delete_note TEMP",
    "delete_note UNREAL",
    "change_note_title IT #ITC",
    "change_note_title UNREAL NEW_TITLE",
    "change_note_text ITC ITC its cool",
    "change_note_text UNREAL new_text",
    "add_note_tags ITC #IT #ITC #DEV #COOL",
    "add_note_tags UNREAL #TAG #TAG",
    "add_note_tags ITC",
    "add_note_tags UNREAL",
    "delete_note_tag ITC #COOL",
    "delete_note_tag ITC #BAD",
    "delete_note_tag UNREAL #Tag",
    "change_note_tag ITC #DEV #FUTURE_DEV",
    "change_note_tag ITC",
    "change_note_tag UNREAL #Tag",
    "add_note Test1 text",
    "add_note_tags Test1 #ITC",
    "add_note Test2 text",
    "add_note_tags Test2 #ITC",
    "add_note Test3 text",
    "add_note_tags Test3 #IT",
    "add_note Test4 text",
    "add_note_tags Test4 #IT",
    "add_note Test5 text",
    "add_note_tags Test5 #IT #ITC",
    "find_note_tag #ITC",
    "find_note_tag #IT",
    "find_note_tag #IT #ITC",
    "sort_note_tag #IT",
    "sort_note_tag #ITC",
    "sort_note_tag #IT #ITC",
    "close",
]

file = os.path.abspath(f"src/bot.py")
# Запуск бота и передача команд
bot_process = subprocess.Popen(
    ["python", file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
)

for command in commands:
    bot_process.stdin.write(command + "\n")
    bot_process.stdin.flush()

# Завершение взаимодействия с ботом
bot_process.stdin.write("close\n")
bot_process.stdin.flush()

# Получение вывода бота
output, _ = bot_process.communicate()

print(output)
