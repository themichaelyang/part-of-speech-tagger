# NLP HW 3: POS tagger
# Michael Yang
# Note to the grader: This code uses Python 3.

# remember to add special cases:
# - beginning of file (begin_sentence)
# - empty line (begin_sentence, end_sentence)
# - end of file (end_sentence)

from frequency_table import FrequencyTable


START_TAG = 'begin_sentence'
END_TAG = 'end_sentence'


class Tagger:
    def __init__(self, pos_filename):
        (pos_word_table, transition_table) = process_pos_file(pos_filename)
        self.pos_word_table = pos_word_table
        self.transition_table = transition_table

def read_words_file(words_filename):
    sentences = []
    current_sentence = []

    with open(words_filename, 'r') as words_file:
        for line in words_file:
            if not line.isspace():
                current_sentence.append(line.strip().lower())
            else:
                sentences.append(current_sentence)
                current_sentence = []
        sentences.append(current_sentence)
        
    return sentences


# pos_tags = [*pos_word_table.table] # unpack keys to get all pos tags
# print(read_pos_file('sentence.pos'))
print(read_words_file('sentence.words'))
