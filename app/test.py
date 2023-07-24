import random
incorrect_answers = ['a', 'b', 'c']
correct_answer = 'd'
options = random.sample(incorrect_answers + [correct_answer], len(incorrect_answers) + 1)
is_correct = correct_answer in options
print(is_correct)