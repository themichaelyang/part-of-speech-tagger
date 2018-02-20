# NLP HW 3: POS tagger
# Michael Yang
# Note to the grader: This code uses Python 3.

# remember to add special cases:
# - beginning of file (begin_sentence)
# - empty line (begin_sentence, end_sentence)
# - end of file (end_sentence)

from tags import *


class Tagger:
    def __init__(self, pos_word_table, transition_table):

        self.pos_word_table = pos_word_table
        self.transition_table = transition_table

        self.pos_tags = [*self.pos_word_table.table]

        self.words = set()
        for pos in self.pos_tags:
            self.words.update(self.pos_word_table.table[pos])

        self.pos_tags += [START_TAG, END_TAG]

    def tag(self, sentences):
        for sentence in sentences:
            tagged_sentence = []
            tags = self.tag_sentence(sentence)
            for i in range(len(tags)):
                tagged_sentence.append((sentence[i], tags[i]))
            yield tagged_sentence

    def tag_sentence(self, sentence):
        viterbi = { tag: [0]*len(sentence) for tag in self.pos_tags } # viterbi[pos][index]
        previous = { tag: [NO_TAG]*len(sentence) for tag in self.pos_tags }

        # init with start tag
        for tag in self.pos_tags:
            viterbi[tag][0] = self.trans_prob(START_TAG, tag) * self.emit_prob(tag, sentence[0])
            previous[tag][0] = START_TAG

        # rest of the sentence
        length = len(sentence)
        for index in range(1, length):
            for tag in self.pos_tags:
                word = sentence[index].lower()
                max_score = 0
                best_prev_tag = NO_TAG

                for prev_tag in self.pos_tags:
                    score = viterbi[prev_tag][index - 1] * self.likelihood(tag, prev_tag, word)

                    if score > max_score:
                        max_score = score
                        best_prev_tag = prev_tag

                viterbi[tag][index] = max_score
                previous[tag][index] = best_prev_tag

        # find the best tags with end tag
        final_score = 0
        final_prev = NO_TAG

        for tag in self.pos_tags:
            score = viterbi[tag][length - 1] * self.trans_prob(tag, END_TAG)
            if score > final_score:
                final_score = score
                final_prev = tag

        return self.backtrack(final_prev, previous, length)

    def backtrack(self, final_pointer, backpointer, length):
        path = [final_pointer]
        ptr = final_pointer
        index = length - 1
        tag = backpointer[final_pointer][length - 1]

        while tag != START_TAG:
            path.insert(0, tag)
            ptr = tag
            index -= 1
            tag = backpointer[ptr][index]

        return path

    def likelihood(self, pos, prev_pos, word):
        pos_given_prev = self.trans_prob(prev_pos, pos)
        pos_given_word = self.emit_prob(pos, word)

        return (pos_given_prev * pos_given_word)

    def trans_prob(self, prev_pos, pos):
        return self.transition_table.get_prob(prev_pos, pos)

    def emit_prob(self, pos, word):
        return self.pos_word_table.get_prob(pos, word)
