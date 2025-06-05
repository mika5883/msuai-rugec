import argparse
from os.path import basename 
import pandas as pd
def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-inp', type=str, help='TSV file path with corrupt and corrected sentences')
    parser.add_argument('-out', default='' ,type=str, help='Where you want to store the output txt files')
    parser.add_argument('-sep', default='\t', type=str, help='Delimiter used in your file (default: tab)')
    args = parser.parse_args()
    return args
def main(args:argparse.ArgumentParser):
	df = pd.read_csv(args.inp, sep=args.sep)
	corrupt = df.corrupt.tolist()
	corrected = df.corrected.tolist()
	name = basename(args.inp)[:-4]
	sp = '/' if args.out else ''
	src_path = args.out + sp + 'src_' + name + '.txt'
	trg_path = args.out + sp + 'trg_' + name + '.txt'
	src = open(src_path, 'w', encoding='utf-8')
	trg = open(trg_path, 'w', encoding='utf-8')
	
	for source, corr in zip(corrupt, corrected):
		src.write(str(source).strip() + '\n')
		trg.write(str(corr).strip() + '\n')
	src.close()
	trg.close()

if __name__ == '__main__':
	args = parse_args()
	main(args)