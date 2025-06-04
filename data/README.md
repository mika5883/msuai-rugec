# Data

* [Kaggle dataset](https://www.kaggle.com/datasets/mika5883/wmt2800) - Here you can find my artificial dataset for pretraining and learn how it was generated. [File](part_corrupt_for_pretrain.tsv) - A part of the dataset is available here.

* **GERA**. It is available [here](https://github.com/ReginaNasyrova/GERA). 

* **RULEC**. Learn about how to get it [here](https://github.com/arozovskaya/RULEC-GEC). It is freely available upon request. Test-set patch to improve quality is [here](https://github.com/Askinkaty/russian_gec/tree/main/data/RULEC-GEC).

* **ReLCo**. [Russian learner corpus ReLCo](https://github.com/Askinkaty/Russian_learner_corpus_ReLCo). 

## Data Conversion

Since the data is in m2 format, one should need to convert it into corrupt-corrected pairs. One can do it with [corr_from_m2.py](scripts/corr_from_m2.py). It accepts `-inp` (a path to an input m2 file) `-out` (path to where we save the corrected text file.), which are required, and `-id` (The id of the target annotator in the m2 file.) which is optional. 

As for the original `RULEC-GEC.test.m2`, I found it need back and forth conversion to .txt pairs and then back to .m2. It's needed because the annotation is in russian but ru errant uses eng notation. It's just for consistency.