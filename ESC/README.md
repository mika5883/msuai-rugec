# ESC pipeline.

* Here is the original [repo](https://github.com/nusnlp/esc) with a guide on installation. I recommend using ERRANT venv to train the pipeline. 

* Make sure this line in `file_utils.py` looks like this (-lang ru). By default, it's 'Russian' in ERRANT. I changed it there to 'ru' but you should probably use 'Russian' instead. `lang='Russian'`.
    ```
    def parse_m2(src, cor, m2_path):
        command = "errant_parallel -orig {orig} -cor {cor} -out {out} -lang {lang}".format(orig=src, cor=cor, out=m2_path, lang='ru')
        subprocess.run(command, shell=True, check=True)
    ```

* I use python 3.10.13 and ERRANT 2.3.0.

# From official REPO

## Installation
This code should be run with Python 3.6. The reason Python 3.6 is needed is because the ERRANT version that is used in the BEA-2019 shared task (v2.0.0) is not compatible with Python >= 3.7

Install this code dependencies by running (**I commented out what is not needed since we should already have the packages needed**):
```.bash
<!-- pip install -r requirements.txt
python -m spacy download en -->
wget https://www.comp.nus.edu.sg/~nlp/sw/m2scorer.tar.gz
tar -xf m2scorer.tar.gz
```
Note that you may need to customize your pytorch installation depending on your CUDA version, read more [here](https://pytorch.org/get-started/previous-versions/). The code may also work with torch < 1.9.0 as only simple pytorch functions are used.

## Retraining the experiments in the paper
For the CoNLL-2014 experiment, run: `export EXP_DIR=conll-exp` .

For the BEA-2019 experiment, run: `export EXP_DIR=bea-exp` .
1. Run the training command: 
```.bash
python run.py --train --data_dir $EXP_DIR/dev-text --m2_dir $EXP_DIR/dev-m2 --model_path $EXP_DIR/models --vocab_path $EXP_DIR/vocab.idx
```
2. Get the prediction on BEA-2019 Dev:
```.bash
python run.py --test --data_dir $EXP_DIR/dev-text --m2_dir $EXP_DIR/dev-m2 --model_path $EXP_DIR/models/model.pt --vocab_path $EXP_DIR/vocab.idx --output_path $EXP_DIR/outputs/dev.out
```
3. Get the F0.5 development score:
```.bash
errant_parallel -ori $EXP_DIR/dev-text/source.txt -cor $EXP_DIR/outputs/dev.out -out $EXP_DIR/outputs/dev.m2
errant_compare -ref bea-full-valid.m2 -hyp $EXP_DIR/outputs/dev.m2
```
4. Get the test prediction:
```.bash
python run.py --test --data_dir $EXP_DIR/test-text --m2_dir $EXP_DIR/test-m2 --model_path $EXP_DIR/models/model.pt --vocab_path $EXP_DIR/vocab.idx --output_path $EXP_DIR/outputs/test.out
```
7. [Evaluate](#evaluation) the test prediction. Replace test_output with $EXP_DIR/outputs/test.out


## Combining your own systems
The simplest way is:
- Create a new experiment directory, then go inside this directory.
- Put your base systems' output on BEA-2019 Dev in a folder called `dev-text`. Please also copy the `source.txt` and `target.txt` from the `bea-exp/dev-text` folder to this new `dev-text` folder.
- Put your base system's output on the test set in a folder called `test-text`. Please also put the source sentences of the dataset you are testing with inside the folder, under the name of `source.txt`.
- Create the `models` and `outputs` folder. At this point, make sure your folder structure is similar to the contents of `bea-exp` or `conll-exp`, with the exceptions of `dev-m2` and `test-m2` (The code will generate these folders automatically). 
- Go back to the parent directory and follow the [guide](#retraining-the-experiments-in-the-paper) above, with the $EXP_DIR replaced with your new folder name.

If you want to customize your experiment setup, please note:
- The code will index all files in the `--data_dir` folder as base systems, except the source file (the default filename is `source.txt`) and the target file (the default filename is `target.txt`).
- The code will only read the contents of `--m2_dir`, not `--data_dir`.  The code will index the files in `--data_dir` and look for the file with same basename on the `--m2_dir`.If the `--m2_dir` does not exist, the code will generate the directory along with the contents from the content of `--data_dir`. Thus, if you make any changes to the content of `--data_dir` after `--m2_dir` was generated, please remove the corresponding file on the `--m2_dir` or the delete the whole `--m2_dir` entirely.
- The file names of the training files and the testing files have to be the same. The file names and the ordering are stored in the vocab file.
- When you run the testing, make sure you run the prediction with the correct model and correct vocab file. Both files are dependent to the base systems you are combining.


## License
The source code and models in this repository are licensed under the GNU General Public License Version 3 (see [License](./LICENSE.txt)). For commercial use of this code and models, separate commercial licensing is also available. Please contact Hwee Tou Ng (nght@comp.nus.edu.sg)