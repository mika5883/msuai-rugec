import pymorphy3
import spacy
import argparse
import pandas as pd
from random import randint
from tqdm import tqdm
# import csv

nlp = spacy.load("ru_core_news_lg")
morph = pymorphy3.MorphAnalyzer()

voices =['actv', 'pssv']
aspects = ['perf', 'impf']
persons = ['1per', '2per', '3per']
tenses = ['futr', 'pres', 'past']
numbers = ['plur', 'sing']
genders = ['masc', 'femn', 'neut']

def identify_verbs(text):
    doc = nlp(text)
    verbs = [(token.text, token.i) for token in doc if token.pos_ == 'VERB']
    return verbs

def modify_verb(verb, aspect=None, tense=None, number=None, person=None, voice=None, gender=None):
    p = morph.parse(verb)[0]
    features = set()

    if aspect:
        features.add(aspect)
    if tense:
        features.add(tense)
    if number:
        features.add(number)
    if person:
        features.add(person)
    if voice:
        features.add(voice)
    if gender:
        features.add(gender)
    
    placeholder = p

    for each in list(features):
      x = p.inflect({each})
      if x:
        placeholder = x

    return placeholder.word if placeholder else verb

def reconstruct_sentence(text, verbs, aspect=None, tense=None, number=None, person=None, voice=None, gender=None):
    doc = nlp(text)
    modified_text = list(text)
    offset = 0

    for verb, index in verbs:
        modified_verb = modify_verb(verb, aspect=aspect, tense=tense, number=number, person=person, voice=voice, gender=gender)
        start_char = doc[index].idx
        end_char = start_char + len(verb)
        
        # Update modified_text with the modified_verb
        modified_text[start_char + offset:end_char + offset] = list(modified_verb)
        
        # Calculate the offset
        offset += len(modified_verb) - len(verb)

    return ''.join(modified_text)

def corrupt(text):
    verbs = identify_verbs(text)
    aspect = aspects[randint(0, len(aspects)-1)]
    tense = tenses[randint(0, len(tenses)-1)]
    number = numbers[randint(0, len(numbers)-1)]
    person = persons[randint(0, len(persons)-1)]
    voice = voices[randint(0, len(voices)-1)]
    gender = genders[randint(0, len(genders)-1)]
    return reconstruct_sentence(text, verbs, aspect=aspect, tense=tense, number=number, person=person, voice=voice, gender=gender)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-inp', type=str)
    parser.add_argument('-out', type=str)
    parser.add_argument('-sep', default='\t\t')
    parser.add_argument('-n', default=None, type=int)
    parser.add_argument('-frac', default=None, type=float)
    parser.add_argument('--clean', action=argparse.BooleanOptionalAction)
    parser.add_argument('--dirty', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    return args

def main(args):
    if args.n and args.frac:
        raise Exception('You should choose either n (n_samples) or frac (fraction of data)')
    df = pd.read_csv(args.inp, sep=args.sep, names=['correct_sent', 'corrupt_sent'])#, quoting=csv.QUOTE_NONE)
    tqdm.pandas(desc = "my bar!")
    if args.n:
        df = df.sample(n=args.n, replace=False, random_state=38)
    elif args.frac:
        df = df.sample(frac=args.frac, replace=True, random_state=38)
    if args.clean:
        df.corrupt_sent = df.correct_sent
        df.corrupt_sent = df.corrupt_sent.progress_map(lambda x: corrupt(str(x)))
    elif args.dirty:
        df.corrupt_sent = df.corrupt_sent.progress_map(lambda x: corrupt(str(x)))
    df.to_csv(args.out, sep='\t', index=False)#, doublequote=False, escapechar=' ')

if __name__ == '__main__':
    args = parse_args()
    main(args)