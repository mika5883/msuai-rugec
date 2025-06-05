# Grammar Error Correction for Russian

# Data

One can read about in [data](data) folder. It has links to get training data. 

# Training

* Everything was run in Yandex Data Sphere but can also work in colab. The dependencies aren't listed as many modules for data science and machine learning are usually installed on such platforms. 
* There are in total 5 different notebooks. Two for pretraining and finetuning T5 using SFT. One for our DPO pipeline with T5. Two for training Qwen. It's preferable to use Qwen3 because it uses unsloth and optimizes memory usage a lot. It is also simpler. 

# Inference

Folder [inference](inference) contains two `.ipynb` files with code to extract prediction from T5 and Qwen models. 

# Evaluation

Evaluation requires installation of ERRANT (`python3`) and/or M2Scorer (`python2`). I recommend setting up virtualenvs for both. 

## ERRANT

* Look [here](https://github.com/Askinkaty/errant). It implements a rule-based edit classifier for Russian and helps inspect model performance in detail. This version is also needed to implement ESC pipeline for Russian since it uses ERRANT annotator internally. If you install base ERRANT, it won't be able to work with Russian texts.
* If you follow the instruction carefully, you shouldn't have problems with requirements.

## M2SCORER. 

* Requires python2. Look [here](https://github.com/nusnlp/m2scorer). It achieves slightly higher scores than ERRANT when assessing model performance. 