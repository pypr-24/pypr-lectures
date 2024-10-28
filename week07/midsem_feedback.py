import numpy as np
import pandas as pd

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



if __name__ == "__main__":
    pass
    # save_as_tab_separated('Mid-semester feedback.csv')
    # scramble_words('Mid-semester feedback_tabs.csv')
