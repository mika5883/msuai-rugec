import pandas as pd
import argparse 
from numpy.random import choice
from random import randint
from tqdm import tqdm
import csv

russian_punctuation = {',': 0.491436521671684,
    '.': 0.130824666898895, 
    ';': 0.06583535378928115, 
    '(': 0.05375878676150632, 
    ')': 0.053931919233470973, 
    '-': 0.03492312802823121, 
    ':': 0.06968004888337634, 
    '': 0.01069843255093615, 
    '!': 0.026792827144770832, 
    '?': 0.03689222134270927, 
    '[': 0.01049644466697738, 
    ']': 0.01049644466697738, 
    "'": 0.004233204361183884}

punct_err_prob = 0.11

del_prob = 0.5
replace_prob = 0.25
insert_prob = 0.25


def num_errors(sent):
    f = [(i,tok) for i,tok in enumerate(sent) if tok in russian_punctuation]
    num = 0
    for _ in f:
        if choice([0, 1], 1, p=[1-punct_err_prob, punct_err_prob]) == 1:
            num += 1
    if num != 0:
        return num,[x[0] for x in f] #+punctuation indices
    else:
        return 1, [x[0] for x in f]


def corrupt(sentence):
    sentence = sentence.split()
    num_ers, punc_indices = num_errors(sentence)
    ers = list(choice(['delete', 'replace', 'insert'], size=num_ers, replace=True, p=[del_prob, replace_prob, insert_prob]))
    # print(ers)
    made_ers = [] #запоминаем индексы токенов, куда внесли ошибки, чтобы потом не повторяться
    for er in ers:
        if er == 'insert':
            ind = randint(0, len(sentence)-1)
            num_it = 0
            if ind in made_ers or ind in punc_indices:                
                while True:
                    if num_it == 10:
                        break
                    ind = randint(0, len(sentence)-1)
                    num_it +=1
                    if ind not in made_ers and ind not in punc_indices:
                        break
            if num_it == 10:
                continue
            made_ers.append(ind)
            sentence[ind] = sentence[ind] + f' {choice(list(russian_punctuation.keys()),size=1, p=list(russian_punctuation.values()))[0]} '
        else:
            possible_indices = list(set(punc_indices).difference(set(made_ers))) #для выбора индексов, в которых не допускали ошибку
            if len(possible_indices) == 0: #
                return ' '.join(' '.join(sentence).split()).strip()
            i = choice(possible_indices, 1)[0]
            if er == 'delete':
                sentence[i] = ''
            else:
                sentence[i] = choice(list(russian_punctuation.keys()), size=1, p=list(russian_punctuation.values()))[0]
            made_ers.append(i)
                
    return ' '.join(' '.join(sentence).split()).strip()
    

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-inp', type=str, required=True)
    parser.add_argument('-sep',  default='\t\t')
    parser.add_argument('-n', type=int, default=1000)
    parser.add_argument('-out', type=str, required=True)
    parser.add_argument('--clean', action=argparse.BooleanOptionalAction)
    parser.add_argument('--dirty', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    return args

def main(args):
    df = pd.read_csv(args.inp, sep=args.sep)#, names=['correct_sent', 'corrupt_sent']), #quoting=csv.QUOTE_NONE)
    df = df.sample(args.n, random_state=43, replace=False)
    tqdm.pandas(desc = "my bar!")
    if args.clean:
        df.corrupt_sent = df.correct_sent
        df.corrupt_sent = df.corrupt_sent.progress_map(lambda x: corrupt(str(x)))
    elif args.dirty:
        df.corrupt_sent = df.corrupt_sent.progress_map(lambda x: corrupt(str(x)))
    df.to_csv(args.out, sep='\t', index=False)#, doublequote=False), #escapechar=' ')
         
if __name__ == '__main__':
    args = parse_args()
    main(args)