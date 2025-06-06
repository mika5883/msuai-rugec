# Grammar Error Correction for Russian

# Data

One can read about it in [data](data) folder. It has links to get training data. 
## Scripts
* install requirements from `requirements.txt`. I use python 3.10.13 for ERRANT and ESC Pipeline training. Set up a venv.  
    ```
    py -m pip install -r requirements.txt
    ```
* To use M2Scorer, install python2. I use 2.7.18. You can also set up a venv and run. 
    ```
    python -m pip install m2scorer
    ```

* to use spacy, one should also install `ru_core_news_lg`. run `py -m spacy download ru_core_news_lg` or go to the official spacy website and download the version you need.

# Training and Inference
* you can install requirements from [requirements.txt](train_inference\requirements.txt)

    ```
    python -m pip install -r train_inference\requirements.txt
    ```
## Training

* There are in total 5 different notebooks for training in [here](train_inference\train). Two for pretraining and finetuning T5 using SFT. One for our DPO pipeline with T5. Two for training Qwen. It's preferable to use Qwen3 because it uses unsloth and optimizes memory usage a lot. It is also simpler. 

## Inference

Folder [inference](train_inference\inference) contains two `.ipynb` files with code to extract prediction from T5 and Qwen models. 


## ESC pipeline.

* Here is the original [repo](https://github.com/nusnlp/esc) with a guide on installation. I recommend using ERRANT venv to train the pipeline. 

* Make sure this line in `file_utils.py` looks like this (-lang ru). By default, it's 'Russian' in ERRANT. I changed it there to 'ru' but you should probably use 'Russian' instead. `lang='Russian'`. s
    ```
    def parse_m2(src, cor, m2_path):
        command = "errant_parallel -orig {orig} -cor {cor} -out {out} -lang {lang}".format(orig=src, cor=cor, out=m2_path, lang='ru')
        subprocess.run(command, shell=True, check=True)
    ```




# Evaluation

Evaluation requires installation of ERRANT (`python3`) and/or M2Scorer (`python2`). I recommend setting up virtualenvs for both. 

## ERRANT

* Look [here](https://github.com/Askinkaty/errant). It implements a rule-based edit classifier for Russian and helps inspect model performance in detail. This version is also needed to implement ESC pipeline for Russian since it uses ERRANT annotator internally. If you install base ERRANT, it won't be able to work with Russian texts.
* If you follow the instruction carefully, you shouldn't have problems with requirements.

## M2SCORER. 

* Requires python2. Look [here](https://github.com/nusnlp/m2scorer). It achieves slightly higher scores than ERRANT when assessing model performance. 

* You can run it like this from your **python2** venv (or you might specify `python2`):
    ```
    python m2scorer/scripts/m2scorer.py test_output GOLD.m2
    ```