# Project 5: String Matching
# Author: Bradley Reeves
# Date: 03/17/2020

import ahocorasick
from nltk.corpus import gutenberg
import numpy as np
import matplotlib.pyplot as plt
from time import time
import os

def find_all(string, patterns):
    for pattern in patterns:
        start = 0
        index = 0
        pattern_pos = [string.find(pattern, start)]
    
        while pattern_pos[index] != -1:
            start = pattern_pos[index] + 1
            index += 1
            pattern_pos.append(string.find(pattern, start))
            #print("At pos %s, string.find found pattern: %s" % (start - 1, pattern))

def main():
    # test-case one: increase file size
    patterns = ['Moby', 'Dick', 'the', 'whale', 'a']
    s = gutenberg.raw("melville-moby_dick.txt")

    # create input files
    num_files = 10
    for i in range(num_files):
        new_file = open("dat/test-input/input-file" + str(i) + ".txt", "w")
        new_file.write(str(np.repeat(s, (i + 1)*2, axis=0)))
        new_file.close()

    sims = 2
    final_ac_times = []
    final_pf_times = []
    for sim in range(sims):
        ac_times = []
        pf_times = []
        sizes = []

        for i in range(num_files):
            s = open("dat/test-input/input-file" + str(i) + ".txt").read()
            sizes.append(os.path.getsize("dat/test-input/input-file" + str(i) + ".txt"))

            # using pyahocorasick
            A = ahocorasick.Automaton()
            for idx, key in enumerate(patterns):
                A.add_word(key, (idx, key))
            A.make_automaton()

            start = time()
            A.iter(s)
            ac_times.append(time() - start)

            '''
            for end_index, (insert_order, original_value) in A.iter(s):
                start_index = end_index - len(original_value) + 1
                print("At pos %s, pyahocorasick found pattern: %s" % (start_index, original_value))
            '''

            # python string.find
            start = time()
            find_all(s, patterns)
            pf_times.append(time() - start)

        # average the runtimes
        final_ac_times = np.mean(np.array([final_ac_times, ac_times]), axis=0) if final_ac_times != [] else ac_times
        final_pf_times = np.mean(np.array([final_pf_times, pf_times]), axis=0) if final_pf_times != [] else pf_times

        # plot runtimes
        fig, ax = plt.subplots()

        coefs1 = np.polynomial.polynomial.polyfit(sizes, final_ac_times, 2)
        ffit1 = np.polynomial.polynomial.polyval(sizes, coefs1)

        coefs2 = np.polynomial.polynomial.polyfit(sizes, final_pf_times, 2)
        ffit2 = np.polynomial.polynomial.polyval(sizes, coefs2)

        lines = ax.plot(sizes, ffit1, 'b-', sizes, ffit2, 'g-')
        ax.set(xlabel="File Size (bytes)", ylabel="Runtime (s)", title="String Matcher: Increasing File Size")
        ax.legend(lines, ("Aho-Corasick", "string.find"))
        ax.grid()

        fig.savefig("out/input_size.png")

    # test-case two: increase number of keywords
    patterns = ['Moby', 'Dick', 'the', 'whale', 'a']
    s = gutenberg.raw("melville-moby_dick.txt")

    inc = [['of', 'to', 'and', 'in', 'is'],
           ['it', 'you', 'that', 'he', 'was'],
           ['for', 'on', 'are', 'with', 'as'],
           ['I', 'his', 'they', 'be', 'at'],
           ['one', 'have', 'this', 'from', 'or'],
           ['had', 'by', 'not', 'word', 'but'],
           ['what', 'some', 'we', 'can', 'out'],
           ['were', 'all', 'there', 'when', 'other'],
           ['up', 'use', 'your', 'how', 'said'],
           ['an', 'each', 'she', 'which', 'do']]


    sims = 2
    final_ac_times = []
    final_pf_times = []
    for sim in range(sims):
        ac_times = []
        pf_times = []
        sizes = []
        for i in range(10):
            sizes.append(len(patterns))

            # using pyahocorasick
            A = ahocorasick.Automaton()
            for idx, key in enumerate(patterns):
                A.add_word(key, (idx, key))
            A.make_automaton()

            start = time()
            A.iter(s)
            ac_times.append(time() - start)

            '''
            for end_index, (insert_order, original_value) in A.iter(s):
                start_index = end_index - len(original_value) + 1
                print("At pos %s, pyahocorasick found pattern: %s" % (start_index, original_value))
            '''

            # python string.find
            start = time()
            find_all(s, patterns)
            pf_times.append(time() - start)

            patterns = patterns + inc[i]

        # average the runtimes
        final_ac_times = np.mean(np.array([final_ac_times, ac_times]), axis=0) if final_ac_times != [] else ac_times
        final_pf_times = np.mean(np.array([final_pf_times, pf_times]), axis=0) if final_pf_times != [] else pf_times

    # plot runtimes
    fig, ax = plt.subplots()

    coefs1 = np.polynomial.polynomial.polyfit(sizes, final_ac_times, 2)
    ffit1 = np.polynomial.polynomial.polyval(sizes, coefs1)

    coefs2 = np.polynomial.polynomial.polyfit(sizes, final_pf_times, 2)
    ffit2 = np.polynomial.polynomial.polyval(sizes, coefs2)

    lines = ax.plot(sizes, ffit1, 'b-', sizes, ffit2, 'g-')
    ax.set(xlabel="Number of Keywords", ylabel="Runtime (s)", title="String Matcher: Increasing Number of Keywords")
    ax.legend(lines, ("Aho-Corasick", "string.find"))
    ax.grid()

    fig.savefig("out/keyword_size.png")

if __name__ == '__main__':
    main()