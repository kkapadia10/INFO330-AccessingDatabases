import sqlite3
import sys

connection = sqlite3.connect('../pokemon.sqlite')
cursor = connection.cursor()

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    # Analyze the pokemon whose pokedex_number is in "arg"

    # You will need to write the SQL, extract the results, and compare
    # Remember to look at those "against_NNN" column values; greater than 1
    # means the Pokemon is strong against that type, and less than 1 means
    # the Pokemon is weak against that type
    for pokemon in sys.argv[1:]:
        strong = []
        weak = []
        if arg.isdigit():
            getName = """SELECT name FROM pokemon WHERE pokedex_number = """ + arg + """;"""
            cursor.execute(getName)
            result = cursor.fetchone()
        else:
            result = [arg]
        pokemon_name = cursor.execute(
            "SELECT name FROM pokemon WHERE id=?", (pokemon,)).fetchone()
        name = pokemon_name[0]
        print("Analyzing " + str(pokemon))

        ids = cursor.execute(
            "SELECT type_id FROM pokemon_type WHERE pokemon_id=?", (pokemon,)).fetchall()
        against = cursor.execute(
            "SELECT * FROM against WHERE type_source_id1=? AND type_source_id2=?",
            (ids[0][0], ids[1][0],)).fetchall()
        val = against[0][2:]
        for i in range(len(val)):
            if val[i] > 1:
                strong.append(types[i])
            elif val[i] < 1:
                weak.append(types[i])
        list = []
        for id in ids:
            exec = cursor.execute(
                "SELECT name FROM type WHERE id=?", (id[0],)).fetchone()
            for ex in exec:
                list.append(ex)
        new_str = ""
        for val in list:
            new_str += val
            new_str += " "
        temp = new_str.rstrip()
        print(name + " (" + temp + ") is strong against " + str(strong) +
              " but weak against " + str(weak))

answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")

connection.close()