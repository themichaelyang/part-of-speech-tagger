# NLP HW 3: POS tagger
# Michael Yang
# Note to the grader: This code uses Python 3.

from tagger import Tagger
from process_pos_file import process_pos_file
from read_words_file import read_words_file
import sys


train = 'training/training.pos'
# train = 'training/WSJ_02-21.pos'
test = 'tests/WSJ_23.words'
# test = 'tests/WSJ_24.words'
# out = 'output/my1532.pos'
out = 'my1532.pos'
# out = 'output/out2.pos'


def tag_file(training_filename, input_filename, output_filename):
    print('Training: ' + training_filename)
    tagger = Tagger(*process_pos_file(training_filename))

    print('Reading input: ' + input_filename)
    sentences = read_words_file(input_filename)

    print('Writing tagged output: ' + output_filename)
    count_tags = 0
    with open(output_filename, 'w') as output_file:
        length = len([word for sent in sentences for word in sent])
        for tagged_sentence in tagger.tag(sentences):
            for (tag, word) in tagged_sentence:
                output_file.write(tag + '\t' + word + '\n')
                count_tags += 1
                show_progress(count_tags / length)
            output_file.write('\n')
    print('Complete! Total tags: ' + str(count_tags) + '.')


def show_progress(percentage):
    sys.stdout.write("\r{0:.2f}% ".format(percentage * 100))
    sys.stdout.flush()


if __name__ == '__main__':
    tag_file(train, test, out)
