import json
import telebot

token = "1655048663:AAGyXzCWImIn2c1H-atHfK75_52E6jD9sH0"

bot = telebot.TeleBot(token)

HELP = """
/help - вывести список доступных команд.
/add <list> <message>[@<category>] - добавить задачу <message> в категорию <category> списка <list>. <category> - необязательный параметр.
/show - показать имеющиеся списки.
/show <list1>[, <list2>, ..., <list#>] - показать содержимое списков <list>...<list#>.
/save - сохранить список.
/load - загрузить список.
"""

todo = {}


def add_task(date, task, category):
    if date not in todo:
        todo[date] = {}
    if category not in todo[date]:
        todo[date][category] = []
    todo[date][category].append(task)


def save_tasks():
    j = json.dumps(todo)
    f = open("todo.json", "w")
    f.write(j)
    f.close()


def load_tasks():
    try:
        f = open("todo.json", "r")
        j = json.loads(f.read())
        f.close()
        for date in j:
            for category in j[date]:
                for task in j[date][category]:
                    add_task(date, task, category)
    except:
        save_tasks()


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=["add"])
def add(message):
    category = ""
    args = message.text.split("@", maxsplit=1)
    if len(args) == 2:
        category = args[1]
    args = args[0].rstrip().split(maxsplit=2)
    if len(args) == 3:
        if len(args[2]) >= 3:
            add_task(args[1].lower(), args[2], category)
            msg = f" в категории \"{category}\"" if len(category) > 0 else ""
            bot.send_message(message.chat.id, f"задача \"{args[2]}\" добавлена к списку \"{args[1]}\"{msg}")
        else:
            bot.send_message(message.chat.id, "[!] описание задачи менее трёх символов")
    else:
        bot.send_message(message.chat.id, "[!] недостаточно аргументов")


@bot.message_handler(commands=["show"])
def show(message):
    args = message.text.split(maxsplit=1)
    if len(args) == 1:
        if len(todo) > 0:
            separator = "\n• "
            answer = "списки:" + separator + separator.join(todo.keys())
            bot.send_message(message.chat.id, answer)
        else:
            bot.send_message(message.chat.id, "[!] в список ничего не добавлено")
    else:
        answer = ""
        args = args[1].split(",")
        for arg in args:
            date = arg.strip()
            if date in todo:
                answer += f"--==={date.upper()}===--"
                for category in todo[date]:
                    for task in todo[date][category]:
                        answer += f"\n[ ] {task}"
                        answer += f"  @{category}" if len(category) > 0 else ""
                answer += "\n"
            else:
                answer += f"[!] нет списка с наименованием {date}\n"
            answer += "\n"

        bot.send_message(message.chat.id, answer)


@bot.message_handler(commands=["save"])
def save(message):
    save_tasks()
    bot.send_message(message.chat.id, "список сохранён")


@bot.message_handler(commands=["load"])
def load(message):
    load_tasks()
    bot.send_message(message.chat.id, "список загружен")


print("Starting up...")
print(f"My API status: {bot.get_me()}")
bot.polling(non_stop=True)


