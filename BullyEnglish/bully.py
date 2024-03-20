#!/usr/bin/python3
"""
Script for solving the English Class minigame from Bully

- Takes a set of letters and produces every possible
    word using word using any subset of the letters
- The auxiliary goal is to do this efficiently,
    i.e. not just brute forcing the alphabet

Notes:
    - All words are between 3-6 letters long (game parameter)
    - The Bully english minigame doesn't actually include every
        possible combination of the given letters, so there are
        some unavoidable false positives (particularly with 3 
        letter words).
        * Also some words are not present in all dictionaries (lei/mewl)
"""
from itertools import permutations
import os
import time

ENLGISH_1 = ['E', 'L', 'L', 'M', 'O', 'W']
ENLGISH_2 = ['F', 'G', 'H', 'I', 'S', 'T']
ENLGISH_3 = ['E', 'I', 'L', 'M', 'S', 'S']
ENLGISH_4 = ['A', 'C', 'N', 'O', 'R', 'Y']
ENLGISH_5 = ['A', 'D', 'E', 'G', 'G', 'R']



def solve(letter_set, dict_file="words.txt"):
    """Search for words in dictionary that can be made from 
    any combination of the given set
    """

    words_by_length = [
    [], # 3
    [], # 4
    [], # 5
    []  # 6
    ]

    words_set = set()

    # Check for dictionary file
    if not os.path.isfile(dict_file):
        print(f"[!] File '{words_txt_file}' not found")
        return None

    # Read each word into dictionary organized by first letter
    with open(dict_file, "r") as file:
        for word in file:
            norm_word = word.strip().upper()
            if 7 > len(norm_word) > 2 and norm_word.isalpha(): # Filter out words that arn't A-Z or arn't between 3-6 character long 
                words_set.add(norm_word)
            else:
                pass

    t0 = time.time()

    # Retrieve every 3/4/5/6 letter permutation of letter set, search for them in dictionary
    for length in range(3, 7):  
        for perm in set(permutations(letter_set, length)): # Converted to set to remove duplicates
            perm = "".join(perm)
            if perm in words_set:
                words_by_length[length - 3].append(perm)

    t1 = time.time()

    # Print words, sorted by length
    for length, words in enumerate(words_by_length):
        print(f"\n{length + 3} letter words ({len(words)})\n------------------")
        for word in words:
            print(word)

    print(f"\n[*] Search complete ({t1 - t0:.3f})")



if __name__ == "__main__":
    solve(ENLGISH_5)
