# Data

* [Kaggle dataset](https://www.kaggle.com/datasets/mika5883/wmt2800) - Here you can find my artificial dataset for pretraining and learn how it was generated. [File](part_corrupt_for_pretrain.rar) - A part of the dataset is available here. Just unarchive it first. **It uses '\t\t' to separate correct and corrupt sentences.**

* **GERA**. It is available [here](https://github.com/ReginaNasyrova/GERA). 

* **RULEC**. Learn about how to get it [here](https://github.com/arozovskaya/RULEC-GEC). It is freely available upon request. Test-set patch to improve quality is [here](https://github.com/Askinkaty/russian_gec/tree/main/data/RULEC-GEC).

* **ReLCo**. [Russian learner corpus ReLCo](https://github.com/Askinkaty/Russian_learner_corpus_ReLCo). It is freely available.

* **cLang-8**. Russian cLang-8 dataset. You can get it following instruction [here](https://github.com/google-research-datasets/clang8).

## Data Conversion

Since the data is in m2 format, one should need to convert it into corrupt-corrected pairs. One can do it with [corr_from_m2.py](scripts/corr_from_m2.py). It accepts `-inp` (a path to an input m2 file) `-out` (path to where we save the corrected text file.), which are required, and `-id` (The id of the target annotator in the m2 file.) which is optional. 

As for the original `RULEC-GEC.test.m2`, I found it needs back and forth conversion to .txt pairs and then back to .m2. It's needed because the annotation is in russian but ru errant uses eng notation. It's just for consistency. It's also important to watch out for the way quotes `''` or hyphens, e.g. in `кто-то`, are handled. If there's a mismatch between tokenization in original m2 files and yours, you will get inaccurate results because the indices in `-hyp` and `-ref` .m2 files won't correspond (if you're using ERRANT. it's a bit different with M2Scorer because it takes source and target .txt and gold .m2). We prefer to separate everything, e.g. `кто-то` becomes `кто - то`. 

# Scripts

* [corr_from_m2.py](data\scripts\corr_from_m2.py). Takes as `-inp` path to .m2 file with correction, `-out` path to output .txt file with corrections

* All `introduce` scripts are a bit tricky since I haven't really worked on them well enough. First things first, look out for doubling quotes when using them consequently (or even just once). pandas adds quotes around quotes. even though they're in the file, pandas processes them correctly. But if you use scripts consequently, they double once again and pandas won't be able to help you get rid of them. I manually delete them after the job is done.


* I recommend using the `noun` script first since its logic rewrites corrupt part with correct one and introduces errors there. This behaviour comes from the fact that we used already corrupted .tsv and don't want an overlap. Other scripts can insert errors into already corrupted sentences if `--dirty` flag is on, otherwise, they will rewrite `corrupt_sent` with `correct_sent` and try to insert errors there. If you're interested, run `py introduce_TYPE_errors.py --help`.
* Example usage (operates on .tsv files with 'correct_sent', 'corrupt_sent' columns)

    ```python
    python introduce_noun_errors.py -inp data\25k_NVP.tsv -sep '\t' -out data\new_25k_NVP.tsv -n 25000
    python introduce_verb_errors.py -inp data\new_25k_NVP.tsv -out data\new_25k_NVP.tsv -sep '\t' -frac 1 --dirty
    python introduce_punct_errors.py -inp data\new_25k_NVP.tsv -out data\new_25k_NVP.tsv -sep '\t' -n 25000 --dirty
    ```
* [tsv_to_m2.py](data\scripts\tsv_to_m2.py). As the name suggests, it is used to get a correction .m2 file from a corrupt-corrected .tsv file. `-sep` is '\t' by default.
    ```
    python tsv_to_m2.py -inp TSV_FILE_PATH -out OUTPUT_M2_PATH
    ```
* [tsv2src_trg.py](data\scripts\tsv2src_trg.py). Divides corrupt-corrected .tsv into 2 separate .txt files for M2Scorer. `-sep` is '\t' by default. src are usually redundant since we already have them but it's fine.
    ```
    python tsv2src_trg.py -inp TSV_FILE_PATH -out OUTPUT_FOLDER
    ```