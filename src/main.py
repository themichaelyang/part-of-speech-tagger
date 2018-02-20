from tagger import Tagger
from process_pos_file import process_pos_file
from read_words_file import read_words_file


train = 'tests/WSJ_24.pos'
test = 'tests/test2.words'
out = 'tests/my1532.pos'
sol = 'tests/WSJ_24.pos'


def tag_file(training_filename, input_filename, output_filename):
    print('Training: ' + training_filename)
    tagger = Tagger(*process_pos_file(training_filename))

    print('Reading input: ' + input_filename)
    sentences = read_words_file(input_filename)

    print('Writing tagged output: ' + output_filename)
    count_tags = 0
    with open(output_filename, 'w') as output_file:
        for tagged_sentence in tagger.tag(sentences):
            for (tag, word) in tagged_sentence:
                output_file.write(tag + '\t' + word + '\n')
                count_tags += 1
            output_file.write('\n')

    print('Complete! Total tags: ' + str(count_tags) + '.')


if __name__ == '__main__':
    tag_file(train, test, out)
