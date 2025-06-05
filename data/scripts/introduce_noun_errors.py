import spacy
import pymorphy3
import argparse 
from tqdm import tqdm 
import pandas as pd
from random import randint

if __name__ == '__main__':
  morph = pymorphy3.MorphAnalyzer()
  nlp = spacy.load('ru_core_news_lg')

def extract_noun_phrases(text, nlp=nlp):
    doc = nlp(text)
    noun_phrases = []

    for token in doc:
        if token.pos_ == 'NOUN':
            noun_phrase = token.text
            left_tokens = [tuple([left.i, left.text]) for left in token.lefts if left.dep_ in ('amod', 'det', 'nummod', 'nmod', 'iobj')]
            right_tokens = [tuple([right.i, right.text]) for right in token.rights if right.dep_ in ('amod', 'det', 'compound', 'nmod', 'iobj')]
            # full_phrase = ' '.join(left_tokens + [noun_phrase] + right_tokens) #initial option but discarded due to sorting/combination issues
            full_phrase = [left_tokens, [tuple([token.i, noun_phrase])], right_tokens] #lots of indices to use later to create revised_noun_phrases
            full_phrase = [a for each in full_phrase for a in each] #flatten
            c = 0 #create a function for this
            container = []
            for ind,ph in enumerate(full_phrase):
              if c == 0:
                container.append(ph)
                c += 1
              else:
                if (ph[0] - full_phrase[ind-1][0]) <= 2:
                  container.append(ph)
            full_phrase = container
            if len(left_tokens) != 0:
              if left_tokens[0][1] == token.text:
                left_tokens.pop(0)
            if len(left_tokens) == 0:
              start_index = token.i
            else:
              start_index = token.left_edge.i
            if len(right_tokens) == 0:
              end_index = token.i
            else:
              end_index = token.right_edge.i
              
            
            noun_phrases.append([full_phrase, start_index, end_index])
    return noun_phrases, text

def revise(noun_phrases, text, nlp=nlp):
    doc = nlp(text)
    # проверка пересечений во фразах для объединения их в одну крупную
    revised_noun_phrases = []
    last_indices = [] #only for 1 last value
    for i, each in enumerate(noun_phrases):
      # print(each, i)
      if i == 0:
        last_indices.append((each[1], each[2]))
        revised_noun_phrases.append((' '.join([w for _, w in each[0]]), each[1], each[2]))
        continue
      else:
        if each[1] in range(last_indices[0][0], last_indices[0][1] + 1) or each[2] in range(last_indices[0][0], last_indices[0][1] + 1):
          each_word_indices = sorted(list(set([ind for ind, _ in each[0]] + [ind for ind, _ in noun_phrases[i-1][0]])), reverse=False)
          each_word_indices = list(range(each_word_indices[0], each_word_indices[-1]+1))

          c = 0
          new_indices = []
          for ind, k in enumerate(each_word_indices):
            if c == 0:
              new_indices.append(k)
              c+= 1
            else:
              if (k - each_word_indices[ind-1]) > 2:
                pass
              else:
                new_indices.append(k)
          each_word_indices = new_indices
          last_indices.pop()
          last_indices.append((each_word_indices[0], each_word_indices[-1])) #renew last indices (each[1], each[2])
          revised_noun_phrases.pop()
          revised_noun_phrases.append((' '.join([doc[ind].text for ind in each_word_indices]), each_word_indices[0], each_word_indices[-1]))
        else: #if no overlaps
          last_indices.pop()
          last_indices.append((each[1], each[2]))
          revised_noun_phrases.append((' '.join([w for _, w in each[0]]), each[1], each[2]))
    return revised_noun_phrases

def change_case_or_number(noun_phrase, case=None, number=None, morph=morph):
    words = noun_phrase.split()
    
    modified_words = []
    w = [words[randint(0, len(words)-1)]] #заменяем только одно слово в группе
    for word in words:
        if word in w:
          p = morph.parse(word)[0]
          if case:
              word = p.inflect({case}).word if p.inflect({case}) else word
          if number:
              word = p.inflect({number}).word if p.inflect({number}) else word
        modified_words.append(word)

    return ' '.join(modified_words)

def reconstruct_sentence(sent, noun_phrases, case=None, number=None, nlp=nlp):
    doc = nlp(sent)
    modified_sent = list(sent)
    offset = 0

    for phrase, start_index, end_index in noun_phrases:
        modified_phrase = change_case_or_number(phrase, case=case, number=number)
        start_char = doc[start_index].idx
        end_char = doc[end_index].idx + len(doc[end_index])
        modified_sent[start_char + offset:end_char + offset] = modified_phrase
        offset += len(modified_phrase) - (end_char - start_char)

    return ''.join(modified_sent)

numbers = ['plur', 'sing']
cases = ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct', 'voct'] #['gent2', 'acc2', 'loc2']
def corrupt(sent:str):
  case = cases[randint(0, len(cases)-1)]
  number = numbers[randint(0, 1)]
  return reconstruct_sentence(sent, revise(*extract_noun_phrases(sent)), case=case, number=number)

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-inp', help='',type=str, required=True)
  parser.add_argument('-sep', help='sep symbol of pandas', default='\t\t')
  parser.add_argument('-n', type=int,help='number of examples (no more than the dataset itself) to corrupt' , default=1000)
  parser.add_argument('-out', type=str,help='output .tsv file', required=True)
  parser.add_argument('-rst', type=int, help='random state', default=42)
  args = parser.parse_args()
  return args

def main(args):
  
  df = pd.read_csv(args.inp, sep=args.sep, names=['correct_sent', 'corrupt_sent'])
  df = df.sample(n=args.n, replace=False, random_state=args.rst)
  tqdm.pandas(desc = "corruption")
  df.correct_sent = df.correct_sent.map(lambda x: str(x))
  df.corrupt_sent = df.correct_sent
  df.corrupt_sent = df.corrupt_sent.progress_map(lambda x: corrupt(str(x)))
  df.to_csv(args.out, sep='\t', index=False)#, doublequote=False, escapechar=' ')

if __name__ == '__main__':
  args = parse_args()
  main(args)