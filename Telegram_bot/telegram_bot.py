import sqlite3
import threading
import time
import random

from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "..."

bot = TeleBot(TOKEN)

conn = sqlite3.connect('Base/Base.sqlite', check_same_thread=False)
cursor = conn.cursor()

lock = threading.Lock()

action_1 = "Повернуть налево"
action_2 = "Повернуть направо"
action_3 = "Пойти прямо"
action_final = "Открыть дверь"
TAKE = "Взять кольцо"
NOT_TAKE = "Не брать кольцо"
OPEN_SHOP = "Открыть магазин"
POTION_HEALING = "Выпить зелье"
DEAD_AGAIN = "Начать заново", "Начать сначала", "/start"
BUY_POTION = "Купить зелье лечения"
BUY_SWORD = "Купить меч"
BUY_RING = "Купить кольцо"
END = "Конец игры"

Some_action = [action_1, action_2, action_3]
FORK_CHOICE = [2, 3, 4]

ANSWER_YES = "Да"
ANSWER_NO = "Нет"
Answers_for_questions = [ANSWER_YES, ANSWER_NO]


CHEST = "Сундук"
IMPASSE = "Тупик"
PASSAGE = "Проход"
MONSTER = "Враг"
LOCATION = [CHEST, CHEST, CHEST, CHEST, CHEST, CHEST, IMPASSE,
            IMPASSE, IMPASSE, MONSTER, MONSTER, MONSTER, MONSTER,
            MONSTER, MONSTER, PASSAGE]

BACK = "Идти назад"
READY = "Готов"

POTION = "зелье"
GOLD = "золото"
IN_CHEST = [POTION, GOLD, GOLD, GOLD]

ATTACK = "Атаковать"
ASSAULT = "Напасть"
PROTECT_YOURSELF = "Защитить себя"


attack_count = 0
open_shop_1 = 0
minotaur_rage_count = 1
sword_count = 1
ring_count = 1
potion = 50
potion_1 = 51
gold_chest = 100
gold_chest_2 = 101
gold_monster = 102
path = 0
x = 0
y = 0
z = 0
g = 0
refresh_skeleton = 1
Enemy_fight_1 = 1
Enemy_fight_2 = 2

id_count = 0
id_count_1 = 0
ID_COUNT = []

count_stage = 2

ATTACK_SLIME = [5, 6, 7]
ATTACK_SKELETON = [5, 6, 7, 8, 9, 10]
ATTACK_MIMIC = [15, 16, 17, 18, 19, 20]
ATTACK_MINOTAUR = [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]


def db_table_val(user_id: int, user_name: str, username: str):
    cursor.execute('INSERT INTO test_1 (user_id, user_name, username) VALUES (?, ?, ?)',
                   (user_id, user_name, username))
    conn.commit()


def update_table(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT user_id FROM test_1 WHERE user_id = ?', (message.chat.id,))
    finally:
        lock.release()
        users = cursor.fetchall()
        if users == []:
            ID_COUNT.append(id_count)
            us_id = message.from_user.id
            us_name = message.from_user.first_name
            username = message.from_user.username

            db_table_val(user_id=us_id, user_name=us_name, username=username)


class Character:
    def __init__(self, level):
        self.level = level
        self.health_points = self.base_health_points * level
        self.health_points_main = self.base_health_points + level * (100 // 2)
        self.attack_power = self.base_attack_power * level
        self.experience = self.base_experience * level
        self.up_experience = self.base_up_experience * (2 ** level)

    def attack(self, target: "Character", message):
        self.attack_power = random.choice(self.base_attack_power) * self.level
        if self == Minotaur_1:
            self.update_minotaur_attack(message)
        bot.send_message(message.chat.id, f"{self.character_name} атакует Странника в ответ "
                                          f"с уроном равным {self.attack_power}."
                                          f"\n\nПосле атаки у Странника осталось "
                                          f"{health_base(message) - self.attack_power} здоровья.")

    def update_minotaur_attack(self, message):
        cursor.execute('UPDATE test_1 SET attack_minotaur_30 = ? WHERE user_id = ?',
                       (self.attack_power, message.chat.id,))
        conn.commit()

    def is_alive(self, message):
        if self == Minotaur_1:
            return minotaur_1_health_points_base(message) > 0
        elif self == Slime_1:
            return slime1_base(message) > 0
        elif self == Slime_2:
            return slime2_base(message) > 0
        elif self == Slime_3:
            return slime3_base(message) > 0
        elif self == Skeleton_1:
            return skeleton1_base(message) > 0
        elif self == Skeleton_2:
            return skeleton2_base(message) > 0
        elif self == Mimic_1:
            return mimic1_base(message) > 0

    def __str__(self):
        return f"{self.character_name}"


class Main(Character):
    base_health_points = 50
    base_attack_power = 10
    base_experience = 0
    base_up_experience = 52
    character_name = "Странник"

    def attack(self, target: "Character", message):
        if target == Minotaur_1:
            bot.send_message(message.chat.id, f"{self.character_name} атакует {target.character_name}а "
                                              f"с уроном равным {attack_base(message)}."
                                              f"\n\nПосле атаки у {target.character_name}а осталось "
                                              f"{minotaur_1_health_points_base(message) - attack_base(message)} здоровья.")
        elif target == Slime_1:
            bot.send_message(message.chat.id, f"{self.character_name} атакует {target.character_name}а "
                                              f"с уроном равным {attack_base(message)}."
                                              f"\n\nПосле атаки у {target.character_name}а осталось "
                                              f"{slime1_base(message) - attack_base(message)} здоровья.")
        elif target == Slime_2:
            bot.send_message(message.chat.id, f"{self.character_name} атакует {target.character_name}а "
                                              f"с уроном равным {attack_base(message)}."
                                              f"\n\nПосле атаки у {target.character_name}а осталось "
                                              f"{slime2_base(message) - attack_base(message)} здоровья.")
        elif target == Slime_3:
            bot.send_message(message.chat.id, f"{self.character_name} атакует {target.character_name}а "
                                              f"с уроном равным {attack_base(message)}."
                                              f"\n\nПосле атаки у {target.character_name}а осталось "
                                              f"{slime3_base(message) - attack_base(message)} здоровья.")
        elif target == Skeleton_1:
            bot.send_message(message.chat.id, f"{self.character_name} атакует {target.character_name}а "
                                              f"с уроном равным {attack_base(message)}."
                                              f"\n\nПосле атаки у {target.character_name}а осталось "
                                              f"{skeleton1_base(message) - attack_base(message)} здоровья.")
        elif target == Skeleton_2:
            bot.send_message(message.chat.id, f"{self.character_name} атакует {target.character_name}а "
                                              f"с уроном равным {attack_base(message)}."
                                              f"\n\nПосле атаки у {target.character_name}а осталось "
                                              f"{skeleton2_base(message) - attack_base(message)} здоровья.")
        elif target == Mimic_1:
            bot.send_message(message.chat.id, f"{self.character_name} атакует {target.character_name}а "
                                              f"с уроном равным {attack_base(message)}."
                                              f"\n\nПосле атаки у {target.character_name}а осталось "
                                              f"{mimic1_base(message) - attack_base(message)} здоровья.")


class Slime(Character):
    base_health_points = 30
    base_attack_power = ATTACK_SLIME
    base_experience = 25
    character_name = "Слайм"
    base_up_experience = 100


class Skeleton(Character):
    base_health_points = 40
    base_attack_power = ATTACK_SKELETON
    base_experience = 50
    character_name = "Скелет"
    base_up_experience = 100

    def reincarnation_skeleton(self, message):
        if self == Skeleton_1:
            update_skeleton_health_respawn_1(message)
        elif self == Skeleton_2:
            update_skeleton_health_respawn_2(message)
        time.sleep(0.2)
        bot.send_message(message.chat.id, "При нанесении последнего удара по скелету, он разваливается. "
                                          "Вы победили. "
                                          "\n\nНо как только вы собираетесь уходить, "
                                          "краем глаза вы замечаете, "
                                          "что кости Скелета начали двигаться и собираться обратно в силуэт. "
                                          "К вашему сожалению, бой продолжается.")
        time.sleep(0.2)
        update_refresh_skeleton_0(message)
        meeting_attack(message)


class Mimic(Character):
    base_health_points = 100
    base_attack_power = ATTACK_MIMIC
    base_experience = 75
    character_name = "Мимик"
    base_up_experience = 100


class Minotaur(Character):
    base_health_points = 300
    base_attack_power = ATTACK_MINOTAUR
    base_experience = 0
    character_name = "Минотавр"
    base_up_experience = 0

    def minotaur_rage(self, message):
        update_minotaur_rage_count_0(message)
        for i in range(len(ATTACK_MINOTAUR)):
            ATTACK_MINOTAUR[i] = ATTACK_MINOTAUR[i] * 2
        bot.send_message(message.chat.id, "Нанеся удар по морде, вы замечаете, как Минотавр пошатнулся и отошёл от вас, "
                                          "держась за неё. Вы думаете что это ваш шанс и "
                                          "хотите продолжить атаку, но в этот момент ваш враг начал издавать "
                                          "свирепый рык, что сотрясает стены и заставляет каменный потолок "
                                          "рушиться. "
                                          "В этот момент вы понимаете, что он разозлился и перешёл в ярость, "
                                          "став сильнее."
                                          "\n\nМинотавр повысил свою силу атаки в 2 раза! Будьте осторожны.")
        time.sleep(0.2)


Slime_1 = Slime(level=1)
Slime_2 = Slime(level=2)
Slime_3 = Slime(level=3)
Slime_4 = Slime(level=4)
Skeleton_1 = Skeleton(level=1)
Skeleton_2 = Skeleton(level=2)
Mimic_1 = Mimic(level=1)
Minotaur_1 = Minotaur(level=1)

Wanderer = Main(level=1)

ENEMY = ["Слайм 1 уровня", "Слайм 2 уровня", "Скелет 1 уровня"]
ENEMY_1 = ["Слайм 2 уровня", "Слайм 3 уровня", "Скелет 2 уровня", "Скелет 2 уровня"]

CHOICE_1 = [Mimic_1, CHEST, CHEST]


def respawn_mobs(message):
    Slime_1.health_points = slime1_base(message)
    Slime_2.health_points = slime2_base(message)
    Slime_3.health_points = slime3_base(message)
    Skeleton_1.health_points = skeleton1_base(message)
    Skeleton_2.health_points = skeleton2_base(message)
    Mimic_1.health_points = mimic1_base(message)
    Minotaur_1.health_points = minotaur_1_health_points_base(message)


def meeting_1(message):
    markup = ReplyKeyboardMarkup(row_width=1)
    markup.add(ATTACK, POTION_HEALING, OPEN_SHOP)
    if attack_count_base(message) == 0:
        update_attack_count_1(message)
    if count_stage_base(message) > 8:
        update_enemy_fight_1(message)
        bot.send_message(message.chat.id, f"Вам встретился {enemy_fight_1_base(message)}, время наносить удар.",
                                          reply_markup=markup)
    else:
        update_enemy_fight(message)
        bot.send_message(message.chat.id, f"Вам встретился {enemy_fight_1_base(message)}, время наносить удар.",
                                          reply_markup=markup)


def meeting_attack(message):
    markup = ReplyKeyboardMarkup(row_width=1)
    markup.add(ATTACK, POTION_HEALING, OPEN_SHOP)
    bot.send_message(message.chat.id, "Враг всё ещё жив, продолжайте атаковать.", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ATTACK)
def skip_step(message):
    if minotaur_1_health_points_base(message) != 300:
        fight(character_1=Wanderer, character_2=Minotaur_1, message=message)
    elif mimic1_base(message) != 100:
        fight(character_1=Wanderer, character_2=Mimic_1, message=message)
    elif enemy_fight_1_base(message) == "Слайм 1 уровня":
        fight(character_1=Wanderer, character_2=Slime_1, message=message)
    elif enemy_fight_1_base(message) == "Слайм 2 уровня":
        fight(character_1=Wanderer, character_2=Slime_2, message=message)
    elif enemy_fight_1_base(message) == "Скелет 1 уровня":
        fight(character_1=Wanderer, character_2=Skeleton_1, message=message)
    elif enemy_fight_1_base(message) == "Слайм 3 уровня":
        fight(character_1=Wanderer, character_2=Slime_3, message=message)
    elif enemy_fight_1_base(message) == "Скелет 2 уровня":
        fight(character_1=Wanderer, character_2=Skeleton_2, message=message)


@bot.message_handler(func=lambda message: message.text in ASSAULT)
def skip_step_1(message):
    fight(character_1=Wanderer, character_2=Minotaur_1, message=message)


def mimic_fight(message):
    markup = ReplyKeyboardMarkup(row_width=1)
    markup.add(PROTECT_YOURSELF)
    bot.send_message(message.chat.id, "Нападение! К сожалению, этот сундук оказался мимиком, "
                                      "время защищаться.", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in PROTECT_YOURSELF)
def mimic_attack(message):
    if attack_count_base(message) == 0:
        update_attack_count_1(message)
    bot.send_message(message.chat.id, f"Благодаря вышей реакции вы смогли защититься "
                                      f"и нанести {attack_base(message) // 2} единиц урона, дав отпор, "
                                      f"но при этом потеряли 20 единиц здоровья.")
    update_mimic_1_health_points_protect(message)
    Mimic_1.health_points -= attack_base(message) // 2
    if health_base(message) <= 0:
        markup = ReplyKeyboardMarkup(row_width=1)
        markup.add("Начать заново")
        bot.send_message(message.chat.id, "К сожалению, вы погибли.", reply_markup=markup)
    markup = ReplyKeyboardMarkup(row_width=1)
    markup.add(ATTACK, POTION_HEALING, OPEN_SHOP)
    bot.send_message(message.chat.id, "Вы снова можете атаковать.", reply_markup=markup)


def fight(character_1: Character, character_2: Character, message):
    update_attack_count_1(message)
    if character_2.is_alive(message):
        character_1.attack(target=character_2, message=message)
        if character_2 == Slime_1:
            update_slime_1_health_points(message)
        elif character_2 == Slime_2:
            update_slime_2_health_points(message)
        elif character_2 == Slime_3:
            update_slime_3_health_points(message)
        elif character_2 == Skeleton_1:
            update_skeleton_1_health_points(message)
        elif character_2 == Skeleton_2:
            update_skeleton_2_health_points(message)
        elif character_2 == Mimic_1:
            update_mimic_1_health_points(message)
        elif character_2 == Minotaur_1:
            update_minotaur_1_health_points(message)
        time.sleep(0.2)
        if (character_2 == Minotaur_1 and 0 < minotaur_1_health_points_base(message) <= 120 and
                minotaur_rage_count_base(message) == 1):
            Minotaur_1.minotaur_rage(message)
        if character_2.is_alive(message):
            if character_2 == Minotaur_1:
                character_2.attack(target=character_1, message=message)
                update_main_health_point_for_minotaur(message)
            else:
                character_2.attack(target=character_1, message=message)
                update_main_health_point_for_enemy(message, character_2=character_2)
            if health_base(message) <= 0:
                markup = ReplyKeyboardMarkup(row_width=1)
                markup.add("Начать заново")
                bot.send_message(message.chat.id, "К сожалению, вы погибли.", reply_markup=markup)
            else:
                time.sleep(0.2)
                meeting_attack(message)
        else:
            if (skeleton1_base(message) <= 0 or skeleton2_base(message) <= 0) and refresh_skeleton_base(message) == 1:
                character_2.reincarnation_skeleton(message=message)
            elif minotaur_1_health_points_base(message) <= 0:
                minotaur_dead(message)
            else:
                if count_stage_base(message) > 8:
                    gold_monster_1 = random.randint(30, 40)
                else:
                    gold_monster_1 = random.randint(15, 20)
                update_mobs(message, gold_monster_1=gold_monster_1)
                respawn_mobs(message)
                Wanderer_base_experience = main_base_experience_base(message) + character_2.experience
                if Wanderer_base_experience >= main_up_experience_base(message):
                    bot.send_message(message.chat.id, f"Вы победили {character_2}а, поздравляем!"
                                                      f"\nВы получили опыт в размере {character_2.experience} единиц. "
                                                      f"\nА также вы получили {gold_monster_1} золотых, "
                                                      f"осмотрев поверженного врага. ")
                    bot.send_message(message.chat.id, f"Ваш уровень повысился, теперь он {level_base(message) + 1}!"
                                                      f"\nВаше максимальное здоровье увеличено на 50."
                                                      f"\nВам восстановилось 50 здоровья.")
                    update_level_up(message, character_2=character_2)
                    bot.send_message(message.chat.id, f"\nДо следующего уровня осталось "
                                                      f"{main_up_experience_base(message) -
                                                         main_base_experience_base(message)} единиц опыта.")

                elif Wanderer_base_experience < main_up_experience_base(message):
                    update_exp(message, character_2=character_2)
                    bot.send_message(message.chat.id, f"Вы победили {character_2}а, поздравляем!"
                                                      f"\nВы получили опыт в размере {character_2.experience} единиц. "
                                                      f"До следующего уровня вам осталось "
                                                      f"{main_up_experience_base(message) -
                                                         main_base_experience_base(message)} единиц опыта."
                                                      f"\nА также вы получили {gold_monster_1} золотых, "
                                                      f"осмотрев поверженного врага. ")
                markup = ReplyKeyboardMarkup(row_width=1)
                markup.add(BACK)
                time.sleep(0.2)
                bot.send_message(message.chat.id, "Пора возвращаться назад.", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in action_final)
def final_fight(message):
    markup = ReplyKeyboardMarkup(row_width=3)
    markup.add(POTION_HEALING, ASSAULT, OPEN_SHOP)
    bot.send_message(message.chat.id, "Аккуратно приоткрывая дверь, вы видите просторную комнату, "
                                      "освещённую факелами с играющим в них пламенем. "
                                      "Они висели на стенах и были направлены в центр комнаты, "
                                      "будто показывая, на что вам стоит обратить внимание. "
                                      "И правда, переведя взор туда, вы начинаете по чуть-чуть видеть пьедестал, "
                                      "на котором, в аккуратном отверстии, виднелось нужное вам кольцо. "
                                      "\n\nОднако, кроме него, в комнате был и ещё один незваный гость, "
                                      "открыв дверь до конца, вы его заметили, это был огромный Минотавр, "
                                      "чей рык вы слышали из-за двери, и который уже обратил свой взор на вас. "
                                      "Вам ничего не остаётся делать, "
                                      "кроме как напасть первым.", reply_markup=markup)


def minotaur_dead(message):
    bot.send_message(message.chat.id, "После вашего последнего удара, Минотавр с грохотом "
                                      "падает на пол, полностью поверженный."
                                      "Эта победа далась вам с трудом, но вы смогли и заслужили награду, "
                                      "что следует за ней. Перед вам лежит кольцо на пьедестале, "
                                      "которое нужно только забрать.")
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.add(TAKE, NOT_TAKE)
    bot.send_message(message.chat.id, "Вы желаете его забрать?", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in TAKE)
def take_final_ring(message):
    markup = ReplyKeyboardMarkup(row_width=1)
    markup.add(END)
    bot.send_message(message.chat.id, "После того как вы взяли кольцо с пьедестала, лабиринт вокруг вас начинает "
                                      "рушиться окончательно. Боясь, что вас задавит обломками, вы собираетесь "
                                      "к выходу откуда пришли, но на ваше удивление "
                                      "и к вашему счастью, кольцо в вашей руке начинает "
                                      "светиться, полностью окутывая вас светом. Спустя некоторое время, "
                                      "вы оказываетесь "
                                      "снаружи, перед входом в лабиринт, чей вход начал стремительно разрушаться. "
                                      "\nПосмотрев на свою руку и увидев в ней кольцо, вы удовлетворённо "
                                      "решаете наполнить свои лёгкие запахом леса, после чего "
                                      "продолжаете своё путешествие, по пути раздумывая как вам поступить с кольцом.",
                                      reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in NOT_TAKE)
def not_take_final_ring(message):
    markup = ReplyKeyboardMarkup(row_width=1)
    markup.add(END)
    bot.send_message(message.chat.id, "Посмотрев на кольцо, вы решаете что оно вам не нужно и лучше оставить "
                                      "эту древнюю силу похороненной под землёй, чтобы в мире не начались "
                                      "беспорядки и вражда, когда о ней прознают. "
                                      "Вокруг вас начинает всё окончательно рушиться, "
                                      "а вы стремитесь к выходу, который, к вашей удаче, ведёт прямиком наружу "
                                      "по прямой дороге."
                                      "\nВыйдя из лабиринта на свежий воздух, выход за вами начал "
                                      "трескаться, и в конечном итоге засыпал сам себя, запечатав вход на долгие и "
                                      "долгие года, десятилетия, а может, даже, и века. "
                                      "Вдохнув запах леса полной грудью, "
                                      "вы отправляетесь в своё следующее путешествие, полные надежд и ожиданий "
                                      "от вашего будущего.", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in END)
def end_game(message):
    markup = ReplyKeyboardMarkup(row_width=1)
    markup.add("Начать сначала")
    bot.send_message(message.chat.id, "P.S. Спасибо что сыграли в это приключение! Желаю вам побольше интересных "
                                      "историй, здоровья и успехов!", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in DEAD_AGAIN)
def send_welcome(message):
    update_table(message)
    print(message)
    re_try(message)
    bot.reply_to(message, "P.S. Если вы хотите начать заново, напишите '/start' либо 'Начать заново'"
                          "\n\nЗдравствуй, Странник, твоё приключение начинается здесь. "
                          "\n\nОднажды, проезжая мимо городов и деревушек, "
                          "вами были услышаны рассказы о таинственном меняющемся лабиринте, "
                          "где можно найти давно потерянную реликвию: кольцо, "
                          "что когда то принадлежало легендарному волшебнику - герою, "
                          "что скончался несколько веков назад."
                          "\n\nИ вот, вы сейчас стоите перед тем самым лабиринтом и решаетесь войти внутрь. "
                          "Для чего вам это кольцо? Решать только вам: продать его, "
                          "использовать заточённую в нём магическую силу, "
                          "а может и совсем для иных целей."
                          "\n\nСпустившись в лабиринт, перед вами сразу же предстаёт развилка с тремя направлениями.")
    markup = ReplyKeyboardMarkup(row_width=1)
    item_button = KeyboardButton(READY)
    markup.add(item_button)
    bot.send_message(message.chat.id, "Вы готовы?", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in READY)
def fork_dungeon_1(message):
    markup = ReplyKeyboardMarkup(row_width=3)
    markup.add(action_1, action_3, action_2, POTION_HEALING, OPEN_SHOP)
    bot_message(message)
    bot.send_message(message.chat.id, "Выберите направление:", reply_markup=markup)


def fork_dungeon_2(message):
    if x_base(message) == 0:
        update_x_1(message)
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.add(action_3, action_2, POTION_HEALING, OPEN_SHOP)
    bot_message(message)
    bot.send_message(message.chat.id, "Выберите направление:", reply_markup=markup)


def fork_dungeon_3(message):
    if y_base(message) == 0:
        update_y_1(message)
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.add(action_1, action_3, POTION_HEALING, OPEN_SHOP)
    bot_message(message)
    bot.send_message(message.chat.id, "Выберите направление:", reply_markup=markup)


def fork_dungeon_4(message):
    if z_base(message) == 0:
        update_z_1(message)
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.add(action_1, action_2, POTION_HEALING, OPEN_SHOP)
    bot_message(message)
    bot.send_message(message.chat.id, "Выберите направление:", reply_markup=markup)


def fork_dungeon_5(message):
    g_values(message)
    markup = ReplyKeyboardMarkup(row_width=1)
    markup.add(action_1, POTION_HEALING, OPEN_SHOP)
    bot_message(message)
    bot.send_message(message.chat.id, "Выберите направление:", reply_markup=markup)


def fork_dungeon_6(message):
    g_values(message)
    markup = ReplyKeyboardMarkup(row_width=1)
    markup.add(action_2, POTION_HEALING, OPEN_SHOP)
    bot_message(message)
    bot.send_message(message.chat.id, "Выберите направление:", reply_markup=markup)


def fork_dungeon_7(message):
    g_values(message)
    markup = ReplyKeyboardMarkup(row_width=1)
    markup.add(action_3, POTION_HEALING, OPEN_SHOP)
    bot_message(message)
    bot.send_message(message.chat.id, "Выберите направление:", reply_markup=markup)


def fork_dungeon_8(message):
    markup = ReplyKeyboardMarkup(row_width=1)
    markup.add(action_final, POTION_HEALING, OPEN_SHOP)
    bot_message(message)
    bot.send_message(message.chat.id, "Выберите направление:", reply_markup=markup)


def bot_message(message):
    time.sleep(0.2)
    bot.send_message(message.chat.id, f"Ваше состояние на данный момент: "
                                      f"\n\nВаш уровень: {level_base(message)}"
                                      f"\n\nВаше здоровье: {health_base(message)}"
                                      f"\n\nВаша сила атаки: {attack_base(message)}"
                                      f"\n\nВаше золото: {gold_sum(message)}"
                                      f"\n\nВаши зелья лечения: {potion_sum(message)}")
    time.sleep(0.2)


@bot.message_handler(func=lambda message: message.text in Some_action)
def fork_for_character(message):
    fork = message.text
    if x_base(message) == 1:
        if fork == action_2:
            update_path_left_right(message)
            random_location(message)
        elif fork == action_3:
            update_path_left_ahead(message)
            random_location(message)
    elif y_base(message) == 1:
        if fork == action_1:
            update_path_left_right(message)
            random_location(message)
        if fork == action_3:
            update_path_right_ahead(message)
            random_location(message)
    elif z_base(message) == 1:
        if fork == action_1:
            update_path_left_ahead(message)
            random_location(message)
        elif fork == action_2:
            update_path_right_ahead(message)
            random_location(message)
    elif g_base(message) == 1:
        update_g_0(message)
        go_ahead(message)
    elif fork == action_1:
        update_path_left(message)
        random_location(message)
    elif fork == action_2:
        update_path_right(message)
        random_location(message)
    elif fork == action_3:
        update_path_ahead(message)
        random_location(message)


def random_location(message):
    location = random.choice(LOCATION)
    if location == "Тупик":
        time.sleep(0.2)
        impasse_go_back(message)
    elif location == "Сундук":
        time.sleep(0.2)
        chest_go_back(message)
    elif location == "Проход":
        time.sleep(0.2)
        go_ahead(message)
    elif location == "Враг":
        time.sleep(0.2)
        meeting_1(message)


def go_ahead(message):
    update_count_stage_2(message)
    if count_stage_base(message) == 8:
        bot.send_message(message.chat.id, "Внимание!"
                                          "\nЛабиринт стал сложнее, будьте аккуратны.")
        time.sleep(0.5)
    if count_stage_base(message) == 14:
        bot.send_message(message.chat.id, "Продвигаясь дальше, вы чувствуете..."
                                          "\nКак приближаетесь к кольцу, будьте аккуратны.")
        time.sleep(0.5)
    if count_stage_base(message) >= 17:
        time.sleep(0.5)
        go_ahead_finish(message)
    elif count_stage_base(message) % 3 == 0:
        time.sleep(0.5)
        go_ahead_1(message)
    else:
        bot.send_message(message.chat.id, "Вы нашли проход дальше! Перед вами вновь предстала развилка, "
                                          "что вы выберете?")
        time.sleep(0.5)
        fork_dungeon_1(message)


def go_ahead_1(message):
    bot.send_message(message.chat.id, "Развилка из трёх дорог превратилась в выбор между двумя следующими, "
                                      "каков будет ваш выбор на этот раз?")
    time.sleep(0.5)
    FORK = random.choice(FORK_CHOICE)
    FORK_1 = FORK
    if FORK_1 == 2:
        fork_dungeon_2(message)
    elif FORK_1 == 3:
        fork_dungeon_3(message)
    elif FORK_1 == 4:
        fork_dungeon_4(message)


def go_ahead_finish(message):
    bot.send_message(message.chat.id, "Наконец развилки были закончены и вы пришли к одной единственной дороге, "
                                      "ведущей к мрачно украшенной двери со страшным рыком из под неё. "
                                      "Вы чувствуете, что именно здесь хранится то таинственное кольцо, "
                                      "за которым вы и пришли, так что без страха вы продолжаете свой путь.")
    fork_dungeon_8(message)


def impasse_go_back(message):
    markup = ReplyKeyboardMarkup(row_width=1)
    markup.add(BACK)
    bot.send_message(message.chat.id, "Вы пришли в тупик, время возвращаться назад.", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in BACK)
def go_back(message):
    time.sleep(0.2)
    if open_shop_1_base(message) == 1:
        update_open_shop_0(message)
        markup = ReplyKeyboardMarkup(row_width=1)
        markup.add(ATTACK, POTION_HEALING, OPEN_SHOP)
        bot.send_message(message.chat.id, "Бой продолжается.", reply_markup=markup)
    elif path_base(message) == "Лево":
        fork_dungeon_2(message)
    elif path_base(message) == "Право":
        fork_dungeon_3(message)
    elif path_base(message) == "Прямо":
        fork_dungeon_4(message)
    elif path_base(message) == "Право и прямо":
        values_property(message)
        fork_dungeon_5(message)
    elif path_base(message) == "Лево и прямо":
        values_property(message)
        fork_dungeon_6(message)
    elif path_base(message) == "Лево и право":
        values_property(message)
        fork_dungeon_7(message)
    else:
        fork_dungeon_1(message)


def chest_go_back(message):
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.add(ANSWER_YES, ANSWER_NO)
    bot.send_message(message.chat.id, "Вы нашли сундук, хотите ли его открыть? "
                                      "За ним вы видите тупик.", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in Answers_for_questions)
def chest_answer(message):
    answer = message.text
    if answer == "Нет":
        markup = ReplyKeyboardMarkup(row_width=1)
        markup.add(BACK)
        bot.send_message(message.chat.id, "Время возвращаться назад.", reply_markup=markup)
    elif answer == "Да":
        if count_stage_base(message) > 8:
            choice = random.choice(CHOICE_1)
            if choice == Mimic_1:
                mimic_fight(message)
            else:
                chest_open(message)
        else:
            chest_open(message)


def chest_open(message):
    markup = ReplyKeyboardMarkup(row_width=1)
    markup.add(BACK)
    reward_for_you = random.choice(IN_CHEST)
    if count_stage_base(message) > 8:
        if reward_for_you == "золото":
            gold_chest_11 = random.randint(75, 100)
            bot.send_message(message.chat.id, f"Поздравляю, вы нашли {reward_for_you} в количестве "
                                              f"{gold_chest_11}!")
            update_gold_chest_2(message, gold_chest_11=gold_chest_11)
        else:
            potion_11 = random.randint(2, 3)
            bot.send_message(message.chat.id, f"Поздравляю, вы нашли {reward_for_you} в количестве "
                                              f"{potion_11}!")
            update_potion_1(message, potion_11=potion_11)
    else:
        if reward_for_you == "золото":
            gold_chest_11 = random.randint(50, 75)
            bot.send_message(message.chat.id, f"Поздравляю, вы нашли {reward_for_you} в количестве "
                                              f"{gold_chest_11}!")
            update_gold_chest(message, gold_chest_11=gold_chest_11)
        else:
            potion_11 = random.randint(1, 2)
            bot.send_message(message.chat.id, f"Поздравляю, вы нашли {reward_for_you} в количестве "
                                              f"{potion_11}!")
            update_potion(message, potion_11=potion_11)
    time.sleep(0.2)
    bot.send_message(message.chat.id, "Время возвращаться назад.", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in OPEN_SHOP)
def open_shop(message):
    if attack_count_base(message) == 1:
        update_open_shop_1(message)
    if sword_count_base(message) == 1 and ring_count_base(message) == 1:
        full_shop(message)
    elif sword_count_base(message) == 0 and ring_count_base(message) == 1:
        shop_buy_sword(message)
    elif sword_count_base(message) == 1 and ring_count_base(message) == 0:
        shop_buy_ring(message)
    else:
        shop_buy_sword_ring(message)


def full_shop(message):
    bot.send_message(message.chat.id, "Вы открыли пространственный магазин, "
                                      "в котором вы можете купить следующие товары:"
                                      "\n\nЗелье лечения."
                                      "\nСтоимость 50 золотых."
                                      "\nВосстанавливает 30 здоровья."
                                      "\n\nМеч, выкованный дворфами."
                                      "\nСтоимость 200 золотых."
                                      "\nУвеличивает вашу силу атаки на 15."
                                      "\n\nКольцо здоровья."
                                      "\nСтоимость 200 золотых."
                                      "\nУвеличивает ваше максимальное здоровье на 100.")
    markup = ReplyKeyboardMarkup(row_width=3)
    markup.add(BUY_POTION, BUY_SWORD, BUY_RING, BACK)
    bot.send_message(message.chat.id, f"Хотите ли что-то приобрести?"
                                      f"\n\nВаше золото: "
                                      f"{gold_sum(message)}",
                     reply_markup=markup)


def shop_buy_sword(message):
    bot.send_message(message.chat.id, "Вы открыли пространственный магазин, "
                                      "в котором вы можете купить следующие товары:"
                                      "\n\nЗелье лечения."
                                      "\nСтоимость 50 золотых."
                                      "\nВосстанавливает 30 здоровья."
                                      "\n\nКольцо здоровья."
                                      "\nСтоимость 200 золотых."
                                      "\nУвеличивает ваше максимальное здоровье на 100.")
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.add(BUY_POTION, BUY_RING, BACK)
    bot.send_message(message.chat.id, f"Хотите ли что-то приобрести?"
                                      f"\n\nВаше золото:"
                                      f" {gold_sum(message)}",
                     reply_markup=markup)


def shop_buy_ring(message):
    bot.send_message(message.chat.id, "Вы открыли пространственный магазин, "
                                      "в котором вы можете купить следующие товары:"
                                      "\n\nЗелье лечения."
                                      "\nСтоимость 50 золотых."
                                      "\nВосстанавливает 30 здоровья."
                                      "\n\nМеч, выкованный дворфами."
                                      "\nСтоимость 200 золотых."
                                      "\nУвеличивает вашу силу атаки на 15.")
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.add(BUY_POTION, BUY_SWORD, BACK)
    bot.send_message(message.chat.id, f"Хотите ли что-то приобрести?"
                                      f"\n\nВаше золото: "
                                      f"{gold_sum(message)}",
                     reply_markup=markup)


def shop_buy_sword_ring(message):
    bot.send_message(message.chat.id, "Вы открыли пространственный магазин, "
                                      "в котором вы можете купить следующие товары:"
                                      "\n\nЗелье лечения."
                                      "\nСтоимость 50 золотых."
                                      "\nВосстанавливает 30 здоровья.")
    markup = ReplyKeyboardMarkup(row_width=1)
    markup.add(BUY_POTION, BACK)
    bot.send_message(message.chat.id, f"Хотите ли что-то приобрести?"
                                      f"\n\nВаше золото: "
                                      f"{gold_sum(message)}",
                     reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in BUY_POTION)
def buy_potion(message):
    if gold_sum(message) < 50:
        bot.send_message(message.chat.id, "У вас недостаточно золота.")
    else:
        update_potion_gold(message)
        bot.send_message(message.chat.id, f"Вы купили зелье лечения."
                                          f"\n\nВаши зелья лечения: {potion_sum(message)}"
                                          f"\n\nВаше золото: "
                                          f"{gold_sum(message)}")


@bot.message_handler(func=lambda message: message.text in BUY_SWORD)
def buy_sword(message):
    if gold_sum(message) < 200:
        bot.send_message(message.chat.id, "У вас недостаточно золота.")
    else:
        update_sword_gold(message)
        bot.send_message(message.chat.id, f"Вы купили Меч дворфов."
                                          f"\n\nВаша сила атаки: {attack_base(message)}"
                                          f"\n\nВаше золото: "
                                          f"{gold_sum(message)}")
        if ring_count_base(message) == 1:
            shop_buy_sword(message)
        else:
            shop_buy_sword_ring(message)


@bot.message_handler(func=lambda message: message.text in BUY_RING)
def buy_ring(message):
    if gold_sum(message) < 200:
        bot.send_message(message.chat.id, "У вас недостаточно золота.")
    else:
        update_ring_gold(message)
        bot.send_message(message.chat.id, f"Вы купили Кольцо здоровья."
                                          f"\n\nВаше здоровье: {health_base(message)}"
                                          f"\n\nВаше золото: "
                                          f"{gold_sum(message)}")
        if sword_count_base(message) == 1:
            shop_buy_ring(message)
        else:
            shop_buy_sword_ring(message)


@bot.message_handler(func=lambda message: message.text in POTION_HEALING)
def potion_health(message):
    if potion_sum(message) == 0:
        bot.send_message(message.chat.id, "У вас нет зелий лечения.")
    else:
        current_health_points = health_base(message)
        health = health_base(message) + 30
        if (health > Wanderer.base_health_points + level_base(message) * (100 // 2)
                and ring_count_base(message) == 1):
            update_health_max(message)
            bot.send_message(message.chat.id, f"Вы восстановили себе "
                                              f"{Wanderer.base_health_points + level_base(message) *
                                                 (100 // 2) - current_health_points} единиц здоровья."
                                              f"\n\nВаши зелья лечения: {potion_sum(message)}"
                                              f"\n\nВаше здоровье максимально.")
        elif (health > Wanderer.base_health_points + level_base(message) * (100 // 2) + 100
              and ring_count_base(message) == 0):
            update_health_max_1(message)
            bot.send_message(message.chat.id, f"Вы восстановили себе "
                                              f"{Wanderer.base_health_points + level_base(message) *
                                                 (100 // 2) + 100 - current_health_points} единиц здоровья."
                                              f"\n\nВаши зелья лечения: {potion_sum(message)}"
                                              f"\n\nВаше здоровье максимально.")
        else:
            update_health_healing(message)
            bot.send_message(message.chat.id, f"Вы восстановили себе 30 единиц здоровья."
                                              f"\n\nВаши зелья лечения: {potion_sum(message)}"
                                              f"\n\nВаше здоровье: {health_base(message)}")


def re_try(message):
    update_all(message)


def update_skeleton_health_respawn_1(message):
    cursor.execute('UPDATE test_1 SET Skeleton_1_health_points = ? WHERE user_id = ?',
                   (Skeleton.base_health_points * Skeleton_1.level // 2, message.chat.id,))
    conn.commit()


def update_skeleton_health_respawn_2(message):
    cursor.execute('UPDATE test_1 SET Skeleton_2_health_points = ? WHERE user_id = ?',
                   (Skeleton.base_health_points * Skeleton_2.level // 2, message.chat.id,))
    conn.commit()


def update_minotaur_rage_count_0(message):
    cursor.execute('UPDATE test_1 SET minotaur_rage_count = ? WHERE user_id = ?',
                   (0, message.chat.id,))
    conn.commit()


def update_refresh_skeleton_0(message):
    cursor.execute('UPDATE test_1 SET refresh_skeleton = ? WHERE user_id = ?',
                   (0, message.chat.id,))
    conn.commit()


def update_attack_count_1(message):
    cursor.execute('UPDATE test_1 SET attack_count = ? WHERE user_id = ?',
                   (1, message.chat.id,))
    conn.commit()


def update_enemy_fight_1(message):
    Enemy_fight_2 = random.choice(ENEMY_1)
    Enemy_fight_1 = Enemy_fight_2
    cursor.execute('UPDATE test_1 SET Enemy_fight_1 = ? WHERE user_id = ?',
                   (Enemy_fight_1, message.chat.id,))
    conn.commit()


def update_enemy_fight(message):
    Enemy_fight_2 = random.choice(ENEMY)
    Enemy_fight_1 = Enemy_fight_2
    cursor.execute('UPDATE test_1 SET Enemy_fight_1 = ? WHERE user_id = ?',
                   (Enemy_fight_1, message.chat.id,))
    conn.commit()


def update_mimic_1_health_points_protect(message):
    cursor.execute('UPDATE test_1 SET Mimic_1_health_points = ?, Wanderer_health_points_main = ? WHERE user_id = ?',
                   (mimic1_base(message) - attack_base(message) // 2, health_base(message) - 20, message.chat.id,))
    conn.commit()


def update_mimic_1_health_points(message):
    cursor.execute('UPDATE test_1 SET Mimic_1_health_points = ? WHERE user_id = ?',
                   (mimic1_base(message) - attack_base(message), message.chat.id,))
    conn.commit()


def update_slime_1_health_points(message):
    cursor.execute('UPDATE test_1 SET Slime_1_health_points = ? WHERE user_id = ?',
                   (slime1_base(message) - attack_base(message), message.chat.id,))
    conn.commit()


def update_slime_2_health_points(message):
    cursor.execute('UPDATE test_1 SET Slime_2_health_points = ? WHERE user_id = ?',
                   (slime2_base(message) - attack_base(message), message.chat.id,))
    conn.commit()


def update_slime_3_health_points(message):
    cursor.execute('UPDATE test_1 SET Slime_3_health_points = ? WHERE user_id = ?',
                   (slime3_base(message) - attack_base(message), message.chat.id,))
    conn.commit()


def update_skeleton_1_health_points(message):
    cursor.execute('UPDATE test_1 SET Skeleton_1_health_points = ? WHERE user_id = ?',
                   (skeleton1_base(message) - attack_base(message), message.chat.id,))
    conn.commit()


def update_skeleton_2_health_points(message):
    cursor.execute('UPDATE test_1 SET Skeleton_2_health_points = ? WHERE user_id = ?',
                   (skeleton2_base(message) - attack_base(message), message.chat.id,))
    conn.commit()


def update_minotaur_1_health_points(message):
    cursor.execute('UPDATE test_1 SET Minotaur_1_health_points = ? WHERE user_id = ?',
                   (minotaur_1_health_points_base(message) - attack_base(message), message.chat.id,))
    conn.commit()


def update_main_health_point_for_minotaur(message):
    cursor.execute('UPDATE test_1 SET Wanderer_health_points_main = ? WHERE user_id = ?',
                   (health_base(message) - minotaur_attack_base(message), message.chat.id,))
    conn.commit()


def update_main_health_point_for_enemy(message, character_2: Character):
    cursor.execute('UPDATE test_1 SET Wanderer_health_points_main = ? WHERE user_id = ?',
                   (health_base(message) - character_2.attack_power, message.chat.id,))
    conn.commit()


def update_mobs(message, gold_monster_1):
    cursor.execute('UPDATE test_1 SET attack_count = ?, refresh_skeleton = ?, '
                   'Slime_1_health_points = ?, Slime_2_health_points = ?, Slime_3_health_points = ?, '
                   'Slime_4_health_points = ?, Skeleton_1_health_points = ?, '
                   'Skeleton_2_health_points = ?, Mimic_1_health_points = ?, '
                   'Minotaur_1_health_points = ?, gold_monster = ? WHERE user_id = ?',
                   (0, 1, 30, 60, 90, 120, 40, 80, 100, 300,
                    gold_monster_base(message) + gold_monster_1, message.chat.id,))
    conn.commit()


def update_level_up(message, character_2: Character):
    cursor.execute('UPDATE test_1 SET Wanderer_level = ?, Wanderer_base_experience = ?, '
                   'Wanderer_up_base_experience = ?, Wanderer_health_points_main = ?, '
                   'Wanderer_attack_power = ? WHERE '
                   'user_id = ?',
                   (level_base(message) + 1,
                    main_base_experience_base(message) + character_2.experience -
                    main_up_experience_base(message),
                    52 * (2 ** level_base(message)),
                    health_base(message) + 50, attack_base(message) +
                    10, message.chat.id,))
    conn.commit()


def update_exp(message, character_2: Character):
    cursor.execute('UPDATE test_1 SET Wanderer_base_experience = ? WHERE user_id = ?',
                   (main_base_experience_base(message) + character_2.experience, message.chat.id,))
    conn.commit()


def g_values(message):
    if g_base(message) == 0:
        cursor.execute('UPDATE test_1 SET g = ? WHERE user_id = ?', (1, message.chat.id,))
        conn.commit()
    elif g_base(message) == 1:
        cursor.execute('UPDATE test_1 SET g = ? WHERE user_id = ?', (0, message.chat.id,))
        conn.commit()


def update_x_1(message):
    cursor.execute('UPDATE test_1 SET x = ? WHERE user_id = ?', (1, message.chat.id,))
    conn.commit()


def update_y_1(message):
    cursor.execute('UPDATE test_1 SET y = ? WHERE user_id = ?', (1, message.chat.id,))
    conn.commit()


def update_z_1(message):
    cursor.execute('UPDATE test_1 SET z = ? WHERE user_id = ?', (1, message.chat.id,))
    conn.commit()


def update_path_left(message):
    cursor.execute('UPDATE test_1 SET path = ? WHERE user_id = ?', ("Лево", message.chat.id,))
    conn.commit()


def update_path_right(message):
    cursor.execute('UPDATE test_1 SET path = ? WHERE user_id = ?', ("Право", message.chat.id,))
    conn.commit()


def update_path_ahead(message):
    cursor.execute('UPDATE test_1 SET path = ? WHERE user_id = ?', ("Прямо", message.chat.id,))
    conn.commit()


def update_path_left_ahead(message):
    cursor.execute('UPDATE test_1 SET path = ? WHERE user_id = ?', ("Лево и прямо", message.chat.id,))
    conn.commit()


def update_path_left_right(message):
    cursor.execute('UPDATE test_1 SET path = ? WHERE user_id = ?', ("Лево и право", message.chat.id,))
    conn.commit()


def update_path_right_ahead(message):
    cursor.execute('UPDATE test_1 SET path = ? WHERE user_id = ?', ("Право и прямо", message.chat.id,))
    conn.commit()


def update_g_0(message):
    cursor.execute('UPDATE test_1 SET g = ? WHERE user_id = ?', (0, message.chat.id,))
    conn.commit()


def update_count_stage_2(message):
    cursor.execute('UPDATE test_1 SET count_stage_2 = ? WHERE user_id = ?',
                   (count_stage_base(message) + 1, message.chat.id,))
    conn.commit()


def values_property(message):
    if x_base(message) == 1:
        cursor.execute('UPDATE test_1 SET x = ? WHERE user_id = ?', (0, message.chat.id,))
        conn.commit()
    if y_base(message) == 1:
        cursor.execute('UPDATE test_1 SET y = ? WHERE user_id = ?', (0, message.chat.id,))
        conn.commit()
    if z_base(message) == 1:
        cursor.execute('UPDATE test_1 SET z = ? WHERE user_id = ?', (0, message.chat.id,))
        conn.commit()


def update_open_shop_0(message):
    cursor.execute('UPDATE test_1 SET open_shop_1 = ? WHERE user_id = ?', (0, message.chat.id,))
    conn.commit()


def update_open_shop_1(message):
    cursor.execute('UPDATE test_1 SET open_shop_1 = ? WHERE user_id = ?', (1, message.chat.id,))
    conn.commit()


def update_gold_chest_2(message, gold_chest_11):
    cursor.execute('UPDATE test_1 SET gold_chest_2 = ? WHERE user_id = ?',
                   (gold_chest_2_base(message) + gold_chest_11, message.chat.id,))
    conn.commit()


def update_potion_1(message, potion_11):
    cursor.execute('UPDATE test_1 SET potion_1 = ? WHERE user_id = ?', (potion_1_base(message) + potion_11,
                                                                        message.chat.id,))
    conn.commit()


def update_gold_chest(message, gold_chest_11):
    cursor.execute('UPDATE test_1 SET gold_chest = ? WHERE user_id = ?',
                   (gold_chest_base(message) + gold_chest_11, message.chat.id,))
    conn.commit()


def update_potion(message, potion_11):
    cursor.execute('UPDATE test_1 SET potion = ? WHERE user_id = ?', (potion_base(message) + potion_11,
                                                                      message.chat.id,))
    conn.commit()


def update_potion_gold(message):
    cursor.execute('UPDATE test_1 SET potion = ?, gold_chest = ? WHERE user_id = ?',
                   (potion_base(message) + 1, gold_chest_base(message) - 50, message.chat.id,))
    conn.commit()


def update_sword_gold(message):
    cursor.execute('UPDATE test_1 SET sword_count = ?, Wanderer_attack_power = ?, gold_chest_2 = ?'
                   ' WHERE user_id = ?',
                   (sword_count_base(message) - 1, attack_base(message) + 15,
                    gold_chest_2_base(message) - 200, message.chat.id,))
    conn.commit()


def update_ring_gold(message):
    cursor.execute('UPDATE test_1 SET ring_count = ?, Wanderer_health_points_main = ?, gold_chest_2 = ?'
                   ' WHERE user_id = ?',
                   (ring_count_base(message) - 1, health_base(message) + 100,
                    gold_chest_2_base(message) - 200, message.chat.id,))
    conn.commit()


def update_health_max(message):
    cursor.execute('UPDATE test_1 SET potion = ?, Wanderer_health_points_main = ?'
                   ' WHERE user_id = ?',
                   (potion_base(message) - 1, Wanderer.base_health_points + level_base(message) * (100 // 2),
                    message.chat.id,))
    conn.commit()


def update_health_max_1(message):
    cursor.execute('UPDATE test_1 SET potion = ?, Wanderer_health_points_main = ?'
                   ' WHERE user_id = ?',
                   (potion_base(message) - 1, Wanderer.base_health_points +
                    level_base(message) * (100 // 2) + 100,
                    message.chat.id,))
    conn.commit()


def update_health_healing(message):
    cursor.execute('UPDATE test_1 SET potion = ?, Wanderer_health_points_main = ?'
                   ' WHERE user_id = ?',
                   (potion_base(message) - 1, health_base(message) + 30, message.chat.id,))
    conn.commit()


def update_all(message):
    cursor.execute('UPDATE test_1 SET Minotaur_1_health_points = ?, Mimic_1_health_points = ?, Wanderer_level = ?, '
                   ' Wanderer_base_experience = ?, Wanderer_health_points_main = ?, '
                   'Wanderer_attack_power = ?, refresh_skeleton = ?, x = ?, y = ?, z = ?, g = ?, '
                   'minotaur_rage_count = ?, '
                   'sword_count = ?, ring_count = ?, attack_count = ?, path = ?, '
                   'gold_chest = ?, gold_chest_2 = ?, gold_monster = ?, '
                   'potion = ?, potion_1 = ?, count_stage_1 = ?, count_stage_2 = ?, attack_minotaur_30 = ?, '
                   'Slime_1_health_points = ?, Slime_2_health_points = ?, Slime_3_health_points = ?, '
                   'Slime_4_health_points = ?, Skeleton_1_health_points = ?, '
                   'Skeleton_2_health_points = ?, Wanderer_up_base_experience = ?, open_shop_1 = ?'
                   'WHERE user_id = ?', (300, 100, 1, 0, 100, 10, 1, 0, 0, 0, 0, 1, 1, 1, 0, "p", 0, 0, 0, 0, 0, 1,
                                         2, 35, 30, 60, 90, 120, 40, 80, 104, 0,
                                         message.chat.id,))
    conn.commit()


def minotaur_attack_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT attack_minotaur_30 FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def slime1_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT Slime_1_health_points FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def slime2_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT Slime_2_health_points FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def slime3_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT Slime_3_health_points FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def skeleton1_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT Skeleton_1_health_points FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def skeleton2_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT Skeleton_2_health_points FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def mimic1_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT Mimic_1_health_points FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def main_up_experience_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT Wanderer_up_base_experience FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def minotaur_rage_count_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT minotaur_rage_count FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def minotaur_1_health_points_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT Minotaur_1_health_points FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def refresh_skeleton_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT refresh_skeleton FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def main_base_experience_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT Wanderer_base_experience FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def ring_count_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT ring_count FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def sword_count_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT sword_count FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def potion_1_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT potion_1 FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def potion_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT potion FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def gold_monster_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT gold_monster FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def gold_chest_2_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT gold_chest_2 FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def gold_chest_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT gold_chest FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def count_stage_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT count_stage_2 FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def attack_count_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT attack_count FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def open_shop_1_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT open_shop_1 FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def path_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT path FROM test_1 WHERE user_id = ?', (message.chat.id,))
        path = cursor.fetchone()
        return path[0]
    finally:
        lock.release()


def gold_sum(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT gold_chest FROM test_1 WHERE user_id = ?', (message.chat.id,))
        gold_chest = int("".join([str(i) for i in cursor.fetchone()]))
        cursor.execute('SELECT gold_chest_2 FROM test_1 WHERE user_id = ?', (message.chat.id,))
        gold_chest_2 = int("".join([str(i) for i in cursor.fetchone()]))
        cursor.execute('SELECT gold_monster FROM test_1 WHERE user_id = ?', (message.chat.id,))
        gold_monster = int("".join([str(i) for i in cursor.fetchone()]))
        return gold_chest + gold_chest_2 + gold_monster
    finally:
        lock.release()


def potion_sum(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT potion FROM test_1 WHERE user_id = ?', (message.chat.id,))
        potion_1 = int("".join([str(i) for i in cursor.fetchone()]))
        cursor.execute('SELECT potion_1 FROM test_1 WHERE user_id = ?', (message.chat.id,))
        potion_2 = int("".join([str(i) for i in cursor.fetchone()]))
        return potion_1 + potion_2
    finally:
        lock.release()


def health_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT Wanderer_health_points_main FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def attack_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT Wanderer_attack_power FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def level_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT Wanderer_level FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def x_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT x FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def y_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT y FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def z_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT z FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def g_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT g FROM test_1 WHERE user_id = ?', (message.chat.id,))
        return int("".join([str(i) for i in cursor.fetchone()]))
    finally:
        lock.release()


def enemy_fight_1_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT Enemy_fight_1 FROM test_1 WHERE user_id = ?', (message.chat.id,))
        enemy_fight_1 = cursor.fetchone()
        return enemy_fight_1[0]
    finally:
        lock.release()


def enemy_fight_2_base(message):
    try:
        lock.acquire(True)
        cursor.execute('SELECT Enemy_fight_2 FROM test_1 WHERE user_id = ?', (message.chat.id,))
        enemy_fight_2 = cursor.fetchone()
        return enemy_fight_2[0]
    finally:
        lock.release()


while True:
    try:
        bot.infinity_polling()
    except Exception as _ex:
        print(_ex)
        time.sleep(5)
