import random


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = ' \033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_hp(self):
        return self.hp

    def get_maxhp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_maxmp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print("\n" + "   " + Bcolors.BOLD + Bcolors.OKGREEN + self.name + Bcolors.ENDC)
        print(Bcolors.OKBLUE + Bcolors.BOLD + "    Actions" + Bcolors.ENDC)
        for item in self.actions:
            print("        " + str(i) + ".", item)
            i += 1

    def choose_magic(self):
        i = 1
        print("\n" + Bcolors.OKBLUE + Bcolors.BOLD + "    Spells" + Bcolors.ENDC)
        for spell in self.magic:
            print("        " + str(i) + ".", spell.name, "(Cost:", str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print("\n" + Bcolors.OKGREEN + Bcolors.BOLD + "    Items" + Bcolors.ENDC)
        for item in self.items:
            print("        " + str(i) + ".", item["item"].name, ":", item["item"].description,
                  " (x" + str(item["quantity"]) + ")")
            i += 1

    def choose_target(self, enemies):
        i = 1
        print("\n" + Bcolors.FAIL + Bcolors.BOLD + "    Target:" + Bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("        " + str(i) + ".", enemy.name)
                i += 1

        choice = int(input("    Choose a target: ")) - 1
        return choice

    def get_enemy_stats(self):
        hp_bar = ""
        bar_ticks = ((self.hp / self.maxhp) * 100) / 2

        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1

        while len(hp_bar) < 50:
            hp_bar += " "

        spaces = (11 - (len(str(self.hp)) + len(str(self.maxhp)))) * " "
        hp_string = spaces + str(self.hp) + "/" + str(self.maxhp)

        print("                     __________________________________________________")
        print(Bcolors.BOLD + self.name + ":  " +
              hp_string + " |" + Bcolors.FAIL + hp_bar + Bcolors.ENDC + "|")

    def get_stats(self):
        hp_bar = ""
        mp_bar = ""
        hp_ticks = ((self.hp / self.maxhp) * 100) / 4
        mp_ticks = ((self.mp / self.maxmp) * 100) / 10

        while hp_ticks > 0:
            hp_bar += "█"
            hp_ticks -= 1

        while len(hp_bar) < 25:
            hp_bar += " "

        while mp_ticks > 0:
            mp_bar += "█"
            mp_ticks -= 1

        while len(mp_bar) < 10:
            mp_bar += " "

        hp_string = ((4 - len(str(self.hp))) * " ") + str(self.hp) + "/" + str(self.maxhp)

        mp_string = ((2 - len(str(self.mp))) * " ") + str(self.mp) + "/" + str(self.maxmp)

        print("                     __________________________              __________")
        print(Bcolors.BOLD + self.name + ":    " +
              hp_string + " |" + Bcolors.OKGREEN + hp_bar + Bcolors.ENDC + "|      " +
              mp_string + " |" + Bcolors.OKBLUE + mp_bar + Bcolors.ENDC + "|")

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.generate_damage()

        pct_health = self.hp / self.maxhp * 100

        if self.mp < spell.cost or spell.type == "white" and pct_health > 50:
            self.choose_enemy_spell()
        else:
            return spell, magic_dmg
