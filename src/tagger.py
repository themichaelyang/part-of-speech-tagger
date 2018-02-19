# NLP HW 3: POS tagger
# Michael Yang
# Note to the grader: This code uses Python 3.

# remember to add special cases:
# - beginning of file (begin_sentence)
# - empty line (begin_sentence, end_sentence)
# - end of file (end_sentence)

from process_pos_file import process_pos_file


START_TAG = 'begin_sentence'
END_TAG = 'end_sentence'
NO_TAG = ''


class Tagger:
    def __init__(self, pos_filename):
        (pos_word_table, transition_table) = process_pos_file(pos_filename)

        self.pos_word_table = pos_word_table
        self.transition_table = transition_table

        self.pos_tags = [*self.pos_word_table.table]

        self.words = set()
        for pos in self.pos_tags:
            self.words.update(self.pos_word_table.table[pos])

        self.pos_tags += [START_TAG, END_TAG]

        # print(self.words)

    def tag_sentence(self, sentence):
        viterbi = { tag: [0]*len(sentence) for tag in self.pos_tags } # viterbi[pos][index]
        backpointer = { tag: [NO_TAG]*len(sentence) for tag in self.pos_tags }

        # init
        for pos in self.pos_tags:
            viterbi[pos][0] = self.likelihood(pos, START_TAG, sentence[0])
            backpointer[pos][0] = START_TAG

        # print(backpointer)

        # find max scores
        for word_index in range(1, len(sentence)):
            for pos in self.pos_tags:

                if self.in_vocab(sentence[word_index]):
                    (max_score, max_prev_pos) = self.max_likelihood(pos, sentence[word_index])
                    viterbi[pos][word_index] = max_score
                    backpointer[pos][word_index] = max_prev_pos
                    # print(max_score)
                else:
                    print(sentence[word_index])
                    raise Exception('OOV word')

        last = len(sentence) - 1
        (best_score, backpointer[END_TAG][last]) = self.max_likelihood(END_TAG, sentence[last])

        print(backpointer)

        return self.retrace(backpointer, END_TAG, last)

    def in_vocab(self, word):
        return word in self.words

    def retrace(self, backpointer, last_tag, last_index):
        path = []
        pos = last_tag
        index = last_index
        back = backpointer[last_tag][last_index]

        print('last: ' + str(last_index))

        while not back == START_TAG:
            print('index: ' + str(index) + ', pos: ' + pos)
            pos = back
            back = backpointer[pos][index]
            index -= 1

            path.insert(0, pos)

        return path

    def max_likelihood(self, current_pos, word):
        max_score = -1
        max_prev_pos = NO_TAG

        for prev_pos in self.pos_tags:
            score = self.likelihood(current_pos, prev_pos, word)

            if score > max_score:
                max_score = score
                max_prev_pos = prev_pos

        return (max_score, max_prev_pos)

    def likelihood(self, pos, prev_pos, word):
        pos_given_prev = self.transition_table.get_prob(prev_pos, pos)
        pos_given_word = self.pos_word_table.get_prob(pos, word)
        return pos_given_prev * pos_given_word

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
# print(read_words_file('sentence.words'))

sentences = read_words_file('sentence.words')
tagger = Tagger('WSJ_02-21.pos')

print('Sentence:')
print(' '.join(sentences[0]))
print(len(sentences[0]))

print('Tags:')
tags = tagger.tag_sentence(sentences[0])
print(tags)
print(len(tags))

print('Tagged sentence:')
for i in range(len(sentences[0])):
    print(sentences[0][i])
    print('^ ' + tags[i])
