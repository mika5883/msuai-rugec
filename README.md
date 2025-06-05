# Grammar Error Correction for Russian

# Data

One can read about in [data](data) folder. It has links to get training data. 

# Training

* Everything was run in Yandex Data Sphere but can also work in colab. The dependencies aren't listed as many modules for data science and machine learning are usually installed on such platforms. 
* There are in total 5 different notebooks. Two for pretraining and finetuning T5 using SFT. One for our DPO pipeline with T5. Two for training Qwen. It's preferable to use Qwen3 because it uses unsloth and optimizes memory usage a lot. It is also simpler. 

# Inference

Folder [inference](inference) contains two `.ipynb` files with code to extract prediction from T5 and Qwen models. 

# Evaluation

Evaluation requires installation of ERRANT (`python3`) and/or M2Scorer (`python2`). I recommend setting up virtualenvs for both. For further instruction I invite you to read the `README` of the [process_and_evaluate](process_and_evaluate) folder. 