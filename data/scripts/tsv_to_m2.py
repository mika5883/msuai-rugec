import argparse
import errant
import pandas as pd
import csv
from tqdm import tqdm

def read_df(tsv_path, sep='\t'):
    return pd.read_csv(tsv_path, sep=sep, dtype=str)#, quoting=csv.QUOTE_NONE)

def noop_edit(id=0):
    # Consistent with CLI's noop edit format
    return f"A -1 -1|||noop|||-NONE-|||REQUIRED|||-NONE-|||{id}"

def df2_m2_batched(df, annotator) -> dict:
    m2_dict = {}
    try:
        orig_texts = df['corrupt_sent'] if 'corrupt_sent' in df.columns else df['corrupt']
        cor_texts = df['correct_sent'] if 'correct_sent' in df.columns else df['corrected']
    except KeyError as e:
        raise ValueError("Missing expected columns in TSV") from e
    orig_texts = [str(a) for a in orig_texts]
    cor_texts = [str(a) for a in cor_texts]
    # Parse original and corrected sentences in batches using annotator.nlp.pipe.
    orig_parsed = list(tqdm(annotator.nlp.pipe(orig_texts, batch_size=64, n_process=4), 
                              total=len(df), desc="Parsing corrupt"))
    cor_parsed = list(tqdm(annotator.nlp.pipe(cor_texts, batch_size=64, n_process=4), 
                             total=len(df), desc="Parsing corrected"))

    # Loop through each example.
    for orig_text, or_p, cor_text, cor_p in tqdm(zip(orig_texts, orig_parsed, cor_texts, cor_parsed), 
                                                   total=len(df), desc="Aligning & classifying"):
        # Build the source sentence in M2 format using tokenized text
        src_line = "S " + " ".join([token.text for token in or_p])
        m2_dict[src_line] = []

        # If the parsed original equals the parsed corrected text, output a noop edit.
        if or_p.text.strip() == cor_p.text.strip():
            m2_dict[src_line].append(noop_edit())
        else:
            # Align using the annotator’s align method. Using 'lev=False' to match the CLI.
            # alignment = annotator.align(or_p, cor_p, lev=False)
            # Merge using the 'rules' strategy to match CLI behavior.
            # edits = annotator.merge(alignment, merging='rules')
            edits = annotator.annotate(or_p, cor_p)
            # For each edit, classify and then output its M2 representation.
            for e in edits:
                # classified_edit = annotator.classify(e)
                # m2_dict[src_line].append(classified_edit.to_m2())
                m2_dict[src_line].append(e.to_m2())
    return m2_dict

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-inp', type=str, help='TSV file path with corrupt and corrected sentences')
    parser.add_argument('-out', type=str, help='Where you want to store the output M2 file')
    parser.add_argument('-sep', default='\t', type=str, help='Delimiter used in your file (default: tab)')
    args = parser.parse_args()
    print(args)
    
    # Load the Errant annotator for Russian (or change to "en" if needed).
    annotator = errant.load('ru')
    
    df = read_df(args.inp, sep=args.sep)
    # Optional: remove leading "grammar:" if present in the corrupt column.
    if 'grammar:' in df.iloc[0]['corrupt']:
        df['corrupt'] = df['corrupt'].map(lambda x: x[9:])
    
    m2_dict = df2_m2_batched(df, annotator)
    
    # Write out the M2 file in the expected format.
    with open(args.out, 'w') as w:
        for src_line, edits in m2_dict.items():
            w.write(src_line.strip() + '\n')
            for edit in edits:
                w.write(edit.strip() + '\n')
            w.write('\n')
