# ESC pipeline.

* Here is the original [repo](https://github.com/nusnlp/esc) with a guide on installation. I recommend using ERRANT venv to train the pipeline. 

* Make sure this line in `file_utils.py` looks like this (-lang ru). By default, it's 'Russian' in ERRANT. I changed it there to 'ru' but you should probably use 'Russian' instead. `lang='Russian'`. s
    ```
    def parse_m2(src, cor, m2_path):
        command = "errant_parallel -orig {orig} -cor {cor} -out {out} -lang {lang}".format(orig=src, cor=cor, out=m2_path, lang='ru')
        subprocess.run(command, shell=True, check=True)
    ```


