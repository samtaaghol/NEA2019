import string


def hash_string(to_hash):

    """
    This function hashes a string.
    """

    chars = string.printable

    hashed = ""

    total = 1

    counter = 1

    for letter in to_hash:

        total *= (chars.index(letter) * counter * len(to_hash)*13)

        counter += 1

        if counter%3 == 0:

            total *= total

    total = str(total)[:30]

    temp_int = ""

    for i in range(len(total)):

        temp_int += total[i]

        if i % 2 != 0:

            hashed += chars[int(temp_int)]

            temp_int = ""

    return hashed
