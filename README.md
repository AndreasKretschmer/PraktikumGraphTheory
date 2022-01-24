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

## Beschreibung
Die Funktion __main__() in gen_class_pipe.py startet die gesamte Auswertung für WP2, WP3, und WP4 (ist auch im Code dokumentiert).

* Funktionsbeschreibungen:
    - 
    ```
    def write_simulation_to_file(path, filename, history)
    ```
    Schreibt eine history in ein angegebenes Verzeichnis und erstellt ggf. das Verzeichnis, falls es noch nicht existiert. 

    - 
    ```
    def load_simulations_from_files(max_files = -1)
    ```
    Liest alle Simulationen aus einem fest hinterlegtem Verzeichnis und gibt eine Liste mit allen Simulationen zurück.

    - 
    ```
    def create_diff_simulations(n)
    ```
    Erstellt neue Simulationen für eine festgelegte Menge n und gibt eine Liste der SImulationen zurück.

    - 
    ```
    def compare_first_leaves(history, candidate)
    ```
    Vergleicht ob ein Ergebnis der recognize-Funktion gleich den tatsächlichen ersten Knoten ist.

    - 
    ```
    def divergence_measure(history, rec_tree)
    ```
    Vergleicht die einzelnen rekonstruierten R-Steps mit den tatsächlichen R-Steps und gibt die Anzahl der gleichen Tripel zurück.

    - 
    ```
    def recognize_histories(histories, first_candidate_only=True, print_info=False, use_modified=False, mode='')
    ```
    Führt die einzelnen recognize-Funktionen für die einzelnen Workpackages aus. Je nach WP wird eine unterschiedliche Konfiguration der recognize Funktion aufgerufen. Die Funktion gibt die Laufzeiten, die Anzahl der ausgeführten Schritte, die Fehler, die Anzahl der gleichen ersten Triple und die Anzahl der gleichen R-Steps pro WP zurück.

    - 
    ```
    def handle_reconstruction_result(rec_tree, history)
    ```
    Organisiert die Auswertung und Analyse der Rekonstruktion einer Simulation. Gibt die Fehler, die Anzahl der gleichen ersten Triple und die Anzahl der gleichen R-Steps pro Simulation zurück.

    - 
    ```
    def handle_reconstruction_success(history, rec_tree, print_info=False)
    ```
    Organisiert die Auswertung und Analyse einer erfolgreichen Rekonstruktion. Gibt die Anzahl der gleichen ersten Triple und die Anzahl der gleichen R-Steps pro Simulation zurück.

    - 
    ```
    def handle_reconstruction_failure(rec_tree, print_info=False)
    ```
    Organisiert die Protokollierung einer fehlerhaften Rekonstruktion.

    - 
    ```
    def average_runtimes(rec_runtimes)
    ```
    Protokolliert die durchschnittlichen Laufzeiten der Rekonstruktionen.

    - 
    ```
    def reconstruction_success_errors(n, err, leaves_equal, common_triplet_cnt)
    ```
    Protokolliert alle Ergebnisse der einzelnen WPs
#### Dependencies

Python >= 3.7

* [Numpy](https://numpy.org)
* [Scipy](http://www.scipy.org/install.html)
* [Matplotlib](https://matplotlib.org/)
* [Timit](https://docs.python.org/3/library/timeit.html)
* [Loguru](https://loguru.readthedocs.io/en/stable/index.html)

