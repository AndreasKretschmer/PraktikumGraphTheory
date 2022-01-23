# Praktikum: Recognize R-Metrics

Silja Ava Schrimer, Alexander Vödisch, Andreas Kretschmer

## Installation

* Als erstes muss [Erbeermet](https://github.com/david-schaller/Erdbeermet) installiert werden.
* In dem gleichen Ordner, indem auch Erdbeermet installiert wurde, muss dann dieses Repository geklont werden und die Simulationen hinzugefügt werden. (Alternativ können die Simulationen auch neu erstellt werden, indem man zeile 278 in gen_class_pipe.py einkommentiert und 279 auskommentiert.)
    - Beispiel:
        - Order
            - Erbeermet
            - PraktikumGraphTheory
            - sim

* Anschließend muss in Erdbeermet.src.erdbeermet.recognition.py folgender Code geändert werden:
    - Zeile 195 muss ersetzt werden mit: 
        ```
        def _find_candidates(D, V, print_info, B={}, use_modified=False):
        ```

    - In Zeile 203 muss folgender Code hinzugefügt werden:
        ``` 
            if (z in B) and use_modified:
                if print_info:
                    print(f'skip{z}')
                continue 
        ```

* Um das Programm zu starten muss gen_class_pipe.py ausgeführt werden
    ```
    python gen_class_pipe.py
    ```


#### Dependencies

Python >= 3.7

* [Numpy](https://numpy.org)
* [Scipy](http://www.scipy.org/install.html)
* [Matplotlib](https://matplotlib.org/)
* [Timit](https://docs.python.org/3/library/timeit.html)
* [Loguru](https://loguru.readthedocs.io/en/stable/index.html)

