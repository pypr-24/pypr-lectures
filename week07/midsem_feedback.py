import numpy as np
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import string

# Code adapted from wordcloud package examples.
# https://github.com/amueller/word_cloud/tree/main
# Accessed 28/10/2024.

# More examples with analysing (messy) text data
# More practice of dealing with reading/writing files
# Use dictionaries/tuples
# Learn how to use a new library!

# Some examples are provided at the bottom of the script to
# better understand new commands I've used in the solution. Try them!


def save_as_tab_separated(filename, output_suffix='_tabs'):
    '''
    Convert comma-separated CSV file to tab-separated
    (for ease of reading/processing as text).
    '''
    # Read the raw datafile
    data = pd.read_csv(filename, encoding='utf-8')
    
    # Remove "response number" column
    data.drop(columns=['Response number'], inplace=True)

    # Replace mis-encoded apostrophes
    for col in data.columns:
        data[col] = data[col].str.replace('&#039;', "'")

    # Save as tab-separated CSV
    data.to_csv(filename.split('.')[0] + output_suffix + '.csv', sep='\t', index=False, encoding='utf-8')


def scramble_words(filename, output_suffix='_scrambled'):
    '''
    Scramble words in mid-semester feedback responses
    to anonymise them.
    '''
    # Read the data file (in tab-separated form)
    with open(filename, 'r', encoding='utf-8') as f:
        responses = f.readlines()

    # Organise the answers by question
    by_question = []

    for question in range(6):

        all_answers = []
        
        # Loop over each student (each row)
        for student in responses:

            # Separate the 6 answers
            answers = student.split(sep='\t')

            # Remove quotation marks and newlines
            words = ''.join([char for char in answers[question] if char not in ['"', '\n']]).split(' ')

            # Concatenate current answer with other answers for the same question
            all_answers += words

        # Create a list of numbers from 0 to the total number of words collected
        scrambler = list(range(len(all_answers)))
        # Shuffle it randomly
        np.random.shuffle(scrambler)

        # Use the shuffled list to scramble all the words
        all_answers = list(np.array(all_answers)[scrambler])
        by_question.append(all_answers)

    # Split the scrambled answers into new "answers" which are 10 words long
    # (for the question with the fewest combined words)
    N_responses = min([len(q) for q in by_question]) // 10
    all_new_answers = []

    for q in by_question:

        # Calculate the number of words per response for the current question
        new_answers = []
        words_per_response = len(q) // N_responses

        # Group the words in single answers with length words_per_response
        for word_index in range(N_responses):
            new_answers.append(q[words_per_response*word_index:words_per_response*(word_index + 1)])

        # Add the final (shorter) answer
        new_answers.append(q[words_per_response*word_index:])
        all_new_answers.append(new_answers)

    # Finally, rebuild the text for the CSV file
    new_text = ''

    for r_index in range(N_responses):

        new_text_answer = ''
        for q_index in range(6):
            new_text_answer += '"' + ' '.join(all_new_answers[q_index][r_index]) + '"\t'

        new_text += new_text_answer + '\n'

    with open(filename.split('.')[0] + output_suffix + '.csv', 'w', encoding='utf-8') as f:
        f.write(new_text)


def make_word_cloud(filename):
    '''
    Create a word cloud from filename.
    '''
    # Read the whole text.
    with open(filename, 'r') as f:
        text = f.read()
    
    # Split answers by student
    all_students = text.rstrip('\n\t').split('\n')
    # print(all_students)

    # Build a dictionary to store answers to the 6 questions
    answers = {'Lecture positives': '',
               'Lecture improvements': '',
               'Materials positives': '',
               'Materials improvements': '',
               'Workshop positives': '',
               'Workshop improvements': ''}
    
    # Set up another dict (with same keys) for words to exclude for each question
    exclude = {'Lecture positives': ['lecture', 'lectures'],
               'Lecture improvements': ['lecture', 'lectures'],
               'Materials positives': ['material', 'materials'],
               'Materials improvements': ['material', 'materials'],
               'Workshop positives': ['workshop', 'workshops'],
               'Workshop improvements': ['workshop', 'workshops']}

    # Split by question for each student
    for student in all_students:
        by_question = student.rstrip('\t').split('\t')
        # assert len(by_question) == 6, by_question

        # Loop over all 6 questions
        for i, q in enumerate(answers.keys()):
            # Append lowercased answer to current question to main string
            answers[q] += by_question[i].lower()
    
    # Now we have a big string containing all student answers for each question.

    # Create a figure to display the word clouds
    fig, ax = plt.subplots(2, 3, figsize=(15, 8))

    # Prepare some indices to plot each question in the appropriate axes
    # (there are better ways to do this -- see iterators later in the course!)
    plot_idx = [[i, j] for j in [0, 1, 2] for i in [0, 1]]
    # print(plot_idx)

    for i, q in enumerate(answers.keys()):
        # Change all punctuation to spaces
        acceptable_chars = string.ascii_lowercase + ' '
        answers[q] = ''.join([char if char in acceptable_chars else ' ' for char in answers[q]])

        # Split each string into words, exclude specific words, rebuild big string
        # by joining words with a space
        answers[q] = ' '.join([word for word in answers[q].split() if word not in exclude[q]])

        # Generate a word cloud image for the current question
        wordcloud = WordCloud(width=600, height=400).generate(answers[q])

        # Plot it in the current axes
        ax[*plot_idx[i]].imshow(wordcloud, interpolation='bilinear')
        ax[*plot_idx[i]].set(title=q)
        ax[*plot_idx[i]].set_axis_off()

    margin = 0.05
    plt.subplots_adjust(top=1-margin, bottom=margin, left=margin, right=1-margin, wspace=margin, hspace=margin)
    plt.show()


if __name__ == "__main__":
    # pass
    # save_as_tab_separated('Mid-semester feedback.csv')
    # scramble_words('Mid-semester feedback_tabs.csv')
    make_word_cloud('week07/Mid-semester feedback_tabs_scrambled.csv')


    # # try this to understand how .join() works to join a list of strings:
    # print('SEPARATOR'.join(['a', 'b', 'c', 'd']))

    # # try this to understand how the * "unpacks" a list into its elements:
    # my_list = [1, 2, 3]
    # print(my_list)
    # print(*my_list)

    # # another example:
    # t = np.arange(1, 10).reshape((3, 3))
    # print(t)
    # index = [1, 2]

    # # this won't work, because it will print t[[1, 2]], which provides
    # # 2 different row indices (1 and 2) but no column indices; therefore
    # # the entire rows 1 and 2 are returned
    # # https://numpy.org/doc/stable/user/basics.indexing.html#integer-array-indexing
    # print(t[index])

    # # solution: to get the element on row 1, column 2, we unpack the index
    # # list using *
    # print(t[*index])