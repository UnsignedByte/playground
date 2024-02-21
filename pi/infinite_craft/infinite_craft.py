import requests
import json
import time
import random
import sqlite3
import logging
import sys
from utils import norm_recipe
import argparse
import datetime
from urllib.parse import quote_plus

# Set up logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
# SEt format for log messages
log_format = logging.Formatter("%(levelname)s:\t%(message)s")
# Set up a handler to write to the console
console_handler = logging.StreamHandler(sys.stderr)
console_handler.setFormatter(log_format)
# Add the handler to the logger
log.addHandler(console_handler)

# ANSI escape codes for color
red = "\033[1;31m"
green = "\033[1;32m"
yellow = "\033[1;33m"
blue = "\033[1;34m"
cyan = "\033[1;36m"
purple = "\033[1;35m"
reset = "\033[1;0m"

# Color for warning, error, and info messages.
logging.addLevelName(
    logging.DEBUG, f"{blue}{logging.getLevelName(logging.DEBUG)}{reset}"
)
logging.addLevelName(
    logging.INFO, f"{green}{logging.getLevelName(logging.INFO)}{reset}"
)
logging.addLevelName(
    logging.WARNING, f"{yellow}{logging.getLevelName(logging.WARNING)}{reset}"
)
logging.addLevelName(
    logging.ERROR, f"{red}{logging.getLevelName(logging.ERROR)}{reset}"
)


def combine(a, b):
    s = requests.Session()
    s.headers.update(
        {
            "Referer": "https://neal.fun/infinite-craft/",
            "Origin": "https://neal.fun",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        }
    )
    for _ in range(10):
        try:
            # print(s.headers)
            r = s.get(
                f"https://neal.fun/api/infinite-craft/pair?first={quote_plus(a)}&second={quote_plus(b)}",
            )
            if r.status_code == 500:
                raise Exception("Internal Server Error")
            elif r.status_code != 200:
                raise TimeoutError(r.status_code)
            j = json.loads(r.content)
            if "emoji" not in j:
                print(a, b, j)
            return (j["result"], j["isNew"], j["emoji"])
        except TimeoutError as e:
            log.error(f"Failed to combine {a} and {b}: {e}")
            log.debug(f"Retrying in 1 Minute")
            time.sleep(60)


# Update the depth of a given element and propogate the change
def recursive_update_depth(cur, con, element, depth):
    # Get the old depth of the element
    # log.debug(f"Updating depth of {element} to {depth}")
    old_depth = cur.execute(
        "SELECT depth FROM elements WHERE text = ?", (element,)
    ).fetchone()[0]

    # If the old depth was smaller, return
    if old_depth <= depth:
        return

    # Update the depth of the element
    cur.execute("UPDATE elements SET depth = ? WHERE text = ?", (depth, element))

    # Find all recipes that use the element
    recipes = cur.execute(
        "SELECT * FROM recipes WHERE input1 = ? OR input2 = ?", (element, element)
    ).fetchall()

    # Propogate the change to the output elements
    for input1, input2, output in recipes:
        # Get the depth of the two input elements
        d1 = cur.execute(
            "SELECT depth FROM elements WHERE text = ?", (input1,)
        ).fetchone()[0]
        d2 = cur.execute(
            "SELECT depth FROM elements WHERE text = ?", (input2,)
        ).fetchone()[0]

        recursive_update_depth(cur, con, output, max(d1, d2) + 1)


def insert_combination(con, cur, a: str, b: str, timer_start=None):
    if timer_start is None:
        timer_start = datetime.datetime.now()
    if a == "Nothing" or b == "Nothing":
        return
    # Sort the elements
    elems = norm_recipe(a, b)

    # If the recipe has already been tried, skip it
    if (
        cur.execute(
            "SELECT COUNT(*) FROM recipes WHERE input1 = ? AND input2 = ?",
            (*elems,),
        ).fetchone()[0]
        > 0
    ):
        return
    try:
        result, is_new, emoji = combine(a, b)
    except Exception as e:
        log.error(f"Failed to combine {a} and {b}: {e}")

        return

    # Insert the new recipe into the database
    cur.execute(
        "INSERT OR IGNORE INTO recipes VALUES (?, ?, ?)",
        (*elems, result),
    )

    new_element = (
        cur.execute(
            "SELECT COUNT(*) FROM elements WHERE text = ?", (result,)
        ).fetchone()[0]
        == 0
    )

    # Get the depth of the input elements
    d1 = cur.execute("SELECT depth FROM elements WHERE text = ?", (a,)).fetchone()[0]
    d2 = cur.execute("SELECT depth FROM elements WHERE text = ?", (b,)).fetchone()[0]

    # Calculate the depth of the new element
    depth = max(d1, d2) + 1

    # Add 1 recipe count to both input elements
    cur.execute(
        "UPDATE elements SET recipe_count = recipe_count + 1 WHERE text = ? OR text = ?",
        (a, b),
    )

    # if the element is new:
    if new_element:
        # Add 1 yield to both input elements
        cur.execute(
            "UPDATE elements SET yield = yield + 1 WHERE text = ? OR text = ?",
            (a, b),
        )

        log.info(
            f"{purple + 'First Discovery' if is_new else green + 'New Element'}\n\t{a} + {b} = {emoji} {result}{reset}"
        )
        # Insert the new element into the database
        cur.execute(
            "INSERT OR IGNORE INTO elements VALUES (?, ?, ?, ?, 0, 0)",
            (result, emoji, is_new, depth),
        )
    else:
        # Check if this element has been created before by the left and right elements
        # If it has, update the yield respectively

        if (
            cur.execute(
                """
            SELECT COUNT(*) FROM recipes WHERE output = ? AND (input1 = ? OR input2 = ?)
                    """,
                (result, a, a),
            ).fetchone()[0]
            > 1
        ):
            cur.execute(
                "UPDATE elements SET yield = yield + 1 WHERE text = ?",
                (a,),
            )
        if (
            cur.execute(
                """
            SELECT COUNT(*) FROM recipes WHERE output = ? AND (input1 = ? OR input2 = ?)
                    """,
                (result, b, b),
            ).fetchone()[0]
            > 1
        ):
            cur.execute(
                "UPDATE elements SET yield = yield + 1 WHERE text = ?",
                (b,),
            )

        log.debug(f"{cyan}{a} + {b} = {emoji} {result}{reset}")
        recursive_update_depth(cur, con, result, depth)

    con.commit()

    # Combine the elements
    time.sleep(
        max(
            0.0,
            random.uniform(0.04, 0.08)
            - (datetime.datetime.now() - timer_start).total_seconds(),
        )
    )


def main():
    # ARguments

    parser = argparse.ArgumentParser(description="Crawl to discover new elements")

    parser.add_argument(
        "--depth",
        type=int,
        default=0,
        help="The depth to start at",
    )

    parser.add_argument(
        "--algorithm",
        type=str,
        default="bfs",
        help="The algorithm to use to discover new elements",
    )

    parser.add_argument(
        "--batch",
        type=int,
        default=10,
        help="The number of elements batch for random algorithms",
    )

    args = parser.parse_args()

    if (args.batch < 1) or (args.depth < 0):
        log.error("Invalid arguments")
        exit(1)

    con = sqlite3.connect("infinite_craft.db")
    cur = con.cursor()

    # Insert default elements if they don't exist
    default = [
        ("Water", "💧"),
        ("Fire", "🔥"),
        ("Wind", "🌬️"),
        ("Earth", "🌍"),
    ]

    for element in default:
        cur.execute(
            "INSERT OR IGNORE INTO elements VALUES (?, ?, 0, 0, 0, 0)",
            element,
        )

    log.info(f"Starting crawler with {args.algorithm} algorithm")

    try:
        if args.algorithm == "bfs":
            depth = args.depth
            while True:
                # Get all elements with the current depth
                delements = cur.execute(
                    "SELECT text FROM elements WHERE depth = ?", (depth,)
                ).fetchall()

                # Get all elements with <= current depth
                lelements = cur.execute(
                    "SELECT text FROM elements WHERE depth <= ?", (depth,)
                ).fetchall()

                depth += 1

                log.info(
                    f"Depth {depth}: {len(delements)} X {len(lelements)} = {len(delements) * len(lelements)} recipes to try"
                )

                count = 0

                # Loop through all possible combinations of elements
                for (a,) in delements:
                    for (b,) in lelements:
                        count += 1

                        if count % 100 == 0:
                            log.debug(
                                f"Progress: {count}/{len(delements) * len(lelements)} ({count / (len(delements) * len(lelements)) * 100:.2f}%)"
                            )

                        insert_combination(con, cur, a, b)
        elif args.algorithm == "random":
            while True:
                a_s = cur.execute(
                    "SELECT text FROM elements ORDER BY RANDOM() LIMIT ?",
                    (args.batch,),
                ).fetchall()
                b_s = cur.execute(
                    "SELECT text FROM elements ORDER BY RANDOM() LIMIT ?",
                    (args.batch,),
                ).fetchall()

                a_s = [x for x, in a_s]
                b_s = [x for x, in b_s]

                for a, b in zip(a_s, b_s):
                    insert_combination(con, cur, a, b)
        elif args.algorithm in ["max-yield", "min-uses"]:
            while True:
                t = datetime.datetime.now()
                # Get all the elements in random order
                elements = cur.execute(
                    'SELECT text FROM elements WHERE text <> "Nothing" ORDER BY RANDOM()'
                ).fetchall()
                elements = [x for x, in elements]

                nelements = len(elements)

                if args.algorithm == "max-yield":
                    # Choose the element with the highest yield
                    _a = cur.execute(
                        """
                        SELECT text, yield, recipe_count FROM elements
                            WHERE text <> "Nothing"
                                AND recipe_count < ?
                            ORDER BY (CAST(yield as REAL) / (recipe_count + 1)) DESC LIMIT ?
                        """,
                        (nelements, args.batch),
                    ).fetchall()
                elif args.algorithm == "min-uses":
                    # Get all the elements with the lowest recipe count
                    _a = cur.execute(
                        """
                        SELECT text, yield, recipe_count FROM elements
                            WHERE text <> "Nothing"
                                AND recipe_count < ?
                                AND recipe_count = (SELECT MIN(recipe_count) FROM elements WHERE recipe_count < ?)
                        """,
                        (
                            nelements,
                            nelements,
                        ),
                    ).fetchall()
                    log.info(
                        f"Pulled {len(_a)} elements with a recipe count of {_a[0][2]}"
                    )

                for a, y, r in _a:
                    if args.algorithm == "max-yield":
                        log.debug(
                            f"Max Yield {y}/{r+1} = {y/(r+1):.2f} element {yellow}{a}{reset}"
                        )
                    elif args.algorithm == "min-uses":
                        log.debug(f"Min Uses {r} element {yellow}{a}{reset}")

                    _b = []
                    if r / nelements < 0.7:
                        # Decently high chance of choosing a random element that has not been tried
                        # Just choose a random element until it works

                        for _ in range(args.batch * 10):
                            bt = random.choice(elements)

                            if (
                                cur.execute(
                                    "SELECT COUNT(*) FROM recipes WHERE input1 = ? AND input2 = ?",
                                    norm_recipe(a, bt),
                                ).fetchone()[0]
                                == 0
                            ):
                                _b.append(bt)
                                if len(_b) == args.batch:
                                    break

                    else:
                        # Get all the recipes that use the element
                        recipes = cur.execute(
                            "SELECT input1, input2 FROM recipes WHERE input1 = ? OR input2 = ?",
                            (a, a),
                        ).fetchall()

                        # Get the other input for the recipe
                        other_elems = set(y if x == a else x for x, y in recipes)

                        elements = set(elements)

                        # Get the elements that are not in the recipes
                        other_elems = list(elements - other_elems)

                        if len(other_elems) < args.batch:
                            _b = other_elems
                        else:
                            # Choose a random element from the set
                            _b = random.sample(other_elems, args.batch)

                    for b in _b:
                        insert_combination(con, cur, a, b, t)
    except KeyboardInterrupt:
        log.info("Exiting...")

        con.close()
        exit(0)


if __name__ == "__main__":
    main()
