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

        self.vocab = set()
        self.oov = set()
        for pos in self.pos_tags:
            self.vocab.update(self.pos_word_table.table[pos])

        self.pos_tags += [START_TAG, END_TAG]

    def tag(self, sentences):
        for sentence in sentences:
            tagged_sentence = []
            tags = self.tag_sentence(sentence)
            for i in range(len(tags)):
                tagged_sentence.append((sentence[i], tags[i]))
            yield tagged_sentence
        print(self.oov)

    def tag_sentence(self, sentence):
        if len(sentence) == 0:
            raise Exception('empty sentence!')

        self.sentence = sentence
        viterbi = { tag: [0]*len(sentence) for tag in self.pos_tags } # viterbi[pos][index]
        previous = { tag: [NO_TAG]*len(sentence) for tag in self.pos_tags }

        # init with start tag
        for tag in self.pos_tags:
            word = sentence[0].lower()
            viterbi[tag][0] = self.trans_prob(START_TAG, tag) * self.emit_prob(tag, word)
            previous[tag][0] = START_TAG

        # rest of the sentence
        length = len(sentence)
        for index in range(1, length):
            is_zero = True
            word = sentence[index].lower()

            for tag in self.pos_tags:
                max_score = 0
                best_prev_tag = NO_TAG

                for prev_tag in self.pos_tags:
                    score = viterbi[prev_tag][index - 1] * self.likelihood(tag, prev_tag, word)

                    if score > max_score:
                        max_score = score
                        best_prev_tag = prev_tag
                        is_zero = False

                viterbi[tag][index] = max_score
                previous[tag][index] = best_prev_tag

            if is_zero:
                max_score = 0
                best_prev_tag = NO_TAG

                print('Failed on: ' + word)
                for tag in self.pos_tags:
                    score = viterbi[prev_tag][index - 1]

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

        if final_score == 0:
            for tag in self.pos_tags:
                score = viterbi[tag][length - 1]
                if score > final_score:
                    final_score = score
                    final_prev = tag

        return self.backtrack(final_prev, previous, length)

    def backtrack(self, final_pointer, backpointer, length):
        if final_pointer == NO_TAG:
            print(self.sentence)

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
        # check if word is in vocabulary
        if word in self.vocab:
            return self.pos_word_table.get_prob(pos, word)
        else:
            # handle OOV words
            self.oov.update(word)

            if any(char.isdigit() for char in word) and pos == 'CD':
                return 0.75

            return self.unigram_prob(pos)

    def unigram_prob(self, pos):
        return self.pos_word_table.get_unigram_prob(pos)
