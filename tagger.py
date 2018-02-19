# NLP HW 3: POS tagger
# Michael Yang
# Note to the grader: This code uses Python 3.

# remember to add special cases:
# - beginning of file (begin_sentence)
# - empty line (begin_sentence, end_sentence)
# - end of file (end_sentence)


START_TAG = 'begin_sentence'
END_TAG = 'end_sentence'


def read_pos_file(pos_filename):
    pos_word_table = {}
    transition_table = {}

    with open(pos_filename, 'r') as pos_file:
        prev_pos = START_TAG

        for line in pos_file:

            if prev_pos == END_TAG:
                prev_pos = START_TAG
            pos = ''

            if not line.isspace():
                (word, pos) = line.strip().split()

                add_to_table(pos_word_table, pos, word.lower())
            else:
                # end of sentence
                pos = END_TAG

            add_to_table(transition_table, prev_pos, pos)
            prev_pos = pos

        add_to_table(transition_table, prev_pos, END_TAG)

    return (pos_word_table, transition_table)


def add_to_table(table, first_key, second_key):
    if first_key in table:
        t2 = table[first_key]

        if second_key in t2:
            t2[second_key] += 1
        else:
            t2[second_key] = 1
    else:
        table[first_key] = { second_key: 1 }


print(read_pos_file('sentence.pos'))
