from nltk.corpus import words
import random
import numpy as np


def get_unique_letter_words(vocab, greens=[]):
    unique = []
    for word in vocab:
        d = {}
        # for letter in word:
        #     d[letter] = 0
        # if len(d.keys()) == 5:
        #     unique.append(word)
        flag = False
        for index in range(5):
            if index in greens or word[index] in d:
                continue
            d[word[index]] = 0
        if len(d.keys()) + len(greens) == 5:
            flag = True

        if flag is True:
            unique.append(word)
    return unique


def get_green_letters(truth, guess):
    op = []
    for i in range(0, 5):
        if truth[i] == guess[i]:
            op.append(i)
    return op


def get_orange_letters(truth, guess, greens):
    op = []
    for i in range(0, 5):
        if i in greens:
            continue
        if guess[i] in truth:
            op.append(i)
    return op


def get_word_map(ip):
    word_map = [{}, {}, {}, {}, {}]
    for word in ip:
        for i in range(0, 5):
            if word[i] not in word_map[i]:
                word_map[i].update({word[i]: []})
            word_map[i][word[i]].append(word)
    return word_map


def get_letter_map(ip):
    pos_map = {}
    for word in ip:
        for letter in word:
            if letter not in pos_map:
                pos_map[letter] = []
            pos_map[letter].append(word)
    return pos_map


the_word = "humor"
eng = words.words()
words = [item.lower() for item in eng if len(item) == 5]
sample_list = get_unique_letter_words(words)
word_map = get_word_map(words)

letter_map = get_letter_map(words)


def remove_blacks_from_universal_set(uni, bl, curr_word):
    alt = set()
    for index in bl:
        alt = alt.union(letter_map[curr_word[index]])
    return uni.difference(alt)


def solve_wordle():
    start_word = random.sample(sample_list, 1)[0]
    already_done = []
    universal_set = set(words)
    curr_word = start_word
    counter = 0
    while curr_word != the_word:
        counter = counter + 1
        already_done.append(curr_word)
        universal_set.difference(already_done)
        green = get_green_letters(the_word, curr_word)
        orange = get_orange_letters(the_word, curr_word, green)
        black = set(range(0, 5)).difference(green).difference(orange)
        universal_set = remove_blacks_from_universal_set(universal_set, black, curr_word)
        if len(green) < 1 and len(orange) < 1:
            curr_word = random.sample(universal_set, 1)[0]
            continue

        if len(green) > 0:
            for index in green:
                universal_set = universal_set.intersection(word_map[index][curr_word[index]])
        if len(orange) > 0:
            for index in orange:
                universal_set = universal_set.difference(word_map[index][curr_word[index]])
        curr_word = random.sample(universal_set, 1)[0]
    return counter


counts = []
for i in range(1000):
    counts.append(solve_wordle())
print(len([item for item in counts if item > 6]))
print(np.mean(counts))
print(np.median(counts))
print(max(counts))
