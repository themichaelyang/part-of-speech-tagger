from frequency_table import FrequencyTable
from tags import *

def process_pos_file(pos_filename):
    pos_word_table = FrequencyTable()
    transition_table = FrequencyTable()
    prev_pos = START_TAG

    with open(pos_filename, 'r') as pos_file:
        for line in pos_file:
            pos = ''

            if prev_pos == END_TAG:
                prev_pos = START_TAG

            if not line.isspace():
                (word, pos) = line.strip().split()
                pos_word_table.add(pos, word.lower())
            else:
                # end of sentence
                pos = END_TAG
            transition_table.add(prev_pos, pos)
            prev_pos = pos

        transition_table.add(prev_pos, END_TAG)

    return (pos_word_table, transition_table)
