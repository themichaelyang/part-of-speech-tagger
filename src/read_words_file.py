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
