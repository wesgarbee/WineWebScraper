import os
import random
from Classes.game import Person, Bcolors
from Classes.magic import Spell
from Classes.inventory import Item


# Create black magic
fire = Spell("Fire", 8, 100, "black")
lightning = Spell("Lightning", 10, 120, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 1200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create white magic
cure = Spell("Cure", 12, 620, "white")
cura = Spell("Cura", 80, 1500, "white")

# Create some items
potion = Item("Health Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Big Health Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Health Potion", "potion", "Heals 500 HP", 500)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP for one party member", 9999)
hielixir = Item("MegaElixir", "elixir", "Fully restores party HP/MP", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

# Create list of magic and items
player_magic = [fire, lightning, blizzard, meteor, quake, cure, cura]
enemy_magic = [fire, lightning, quake, cure]
player_items = [potion, hipotion, superpotion, elixir, hielixir, grenade]
player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 2},
                {"item": elixir, "quantity": 5},
                {"item": hielixir, "quantity": 2},
                {"item": grenade, "quantity": 5}]

# Instantiate people
player1 = Person("Oscar", 3000, 85, 132, 34, player_magic, player_items)
player2 = Person("Bert ", 2000, 65, 188, 34, player_magic, player_items)
player3 = Person("Ernie", 2000, 55, 174, 34, player_magic, player_items)

enemy1 = Person("Stan", 11200, 65, 634, 25, enemy_magic, [])
enemy2 = Person("Pete", 1200, 130, 560, 325, enemy_magic, [])
enemy3 = Person("Carl", 1200, 130, 560, 325, enemy_magic, [])

players = [player1, player2, player3]
enemies = [enemy2, enemy1, enemy3]

running = True

print(Bcolors.FAIL + Bcolors.BOLD + "ENEMY APPROACHES!" + Bcolors.ENDC)

while running:
    # os.system('clear')
    print("=============    ==========")

    print("Name                 HP                                      MP")
    for player in players:
        player.get_stats()

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:

        player.choose_action()
        choice = input("    Choose action: ")
        if choice is None:
            continue
        else:
            index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)

            print(player.name + " attacked for", dmg, "points of damage.")

            # Removes the defeated enemy from the list.
            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + " has died.")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(Bcolors.FAIL + "\nNot enough MP\n" + Bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(Bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "points" + Bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(Bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg),
                      "points of damage to", enemies[enemy].name + Bcolors.ENDC)

                # Removes the enemy from the list if defeated
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died.")
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose an item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(Bcolors.FAIL + "\n" + "You have none left..." + Bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(Bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP", Bcolors.ENDC)
            elif item.type == "elixir":

                if item.name == "MegaElixir":
                    for person in players:
                        person.hp = person.maxhp
                        person.mp = person.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(Bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + Bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(Bcolors.FAIL + "\n" + item.name + " deals", str(item.prop),
                      "points of damage to", enemies[enemy].name + Bcolors.ENDC)

                # Removes the enemy from the list if defeated
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died.")
                    del enemies[enemy]

    # Determines if game has ended
    defeated_players = 0
    defeated_enemies = 0

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    # Check if player won
    if defeated_players == len(players):
        print(Bcolors.FAIL + "Your enemies have defeated you!" + Bcolors.ENDC)
        running = False
    # Check if enemy won
    elif defeated_enemies == len(enemies):
        print(Bcolors.OKGREEN + "You have defeated your foes!" + Bcolors.ENDC)
        running = False

    # Enemy controller
    for enemy in enemies:
        enemy_choice = random.randrange(0, 3)

        if enemy_choice == 0:
            # Choose attack
            target = random.randrange(0, len(players))
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(enemy.name + " attacks", players[target].name, "for", enemy_dmg, "points of damage.")

            if players[target].get_hp() == 0:
                print(players[target].name, "has died.")
                del players[target]

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(Bcolors.OKBLUE + "\n" + spell.name + " heals", enemy.name,
                      "for", str(magic_dmg), "points" + Bcolors.ENDC)
            elif spell.type == "black":
                # Selects a player target randomly
                target = random.randrange(0, len(players))

                players[target].take_damage(magic_dmg)

                print(Bcolors.OKBLUE + "\n" + enemy.name + "'s", spell.name, "deals", str(magic_dmg),
                      "points of damage to", players[target].name + Bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name, "has died.")
                    del players[target]

            # print(enemy.name, "chose", spell.name, "and damage is", str(magic_dmg))
        elif enemy_choice == 2:
            print(enemy.name, "says, 'Yawn, pass.'")
