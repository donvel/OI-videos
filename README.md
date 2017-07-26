## Zestaw skryptów do (pół)automatycznej obróbki omówień video na OI i PA

### Wymagania

 - Python 3
 - FFmpeg (używałem wersji 3.2.5-1 na Linuxie)
 - Blender (używałem wersji 2.78c na Linuxie)

### Workflow

Składa się z dwóch części:
1. Wycięcia kadrów z plików video (i od razu przekonwertowania ich do sensownego formatu)
   za pomocą ffmpeg.
2. Sklejenia tych kadrów wraz z dodatkami (czołówka, tyłówka, pasek z afiliacją)
   za pomocą blendera.

Sensowne wydawałoby się pominięcie pierwszej części (zajmuje sporo czasu)
i zrobienie od razu wszystkiego w Blenderze, ale tak wydaje się bardziej stabilnie --
edytory video, których używałem (kdenlive, openshot i właśnie blender) kiepsko
sobie radzą z wycinaniem video z plików .MTS, a takie produkowała kamera, której używałem.
Np. zdarzało się, że dźwięk rozjeżdżał się z wizją, a ffmpeg nie ma takich problemów.

#### Wycinanie kardów
Opróćz "surowych plików wideo" kamerzysta powinien dostarczyć plik tekstowy
z "minutkami". Taki plik składa się z linii pasujących do wyrażenia regularnego
```
(\w+.\w+) (\d+):(\d+) (\d+):(\d+) (\w+)$
```
o następującym znaczeniu:
```
(nazwa pliku wideo) 
(minuta):(sekunda początku ujęcia)
(minuta):(sekunda końca ujęcia)
(opis ujęcia)
```
np. 
```
00341.MTS 00:01 01:26 tresc_zadania
```
większy przykład można znaleźć w pliku [przykladowe\_czasy.txt](przykladowe_czasy.txt).

Kiedy mamy co trzeba, należy wywołać:
```
./slice.py plik-z-czasami folder-docelowy,
```
wtedy skrypt będzie wypisywał i wykonywał polecenia,
które kolejno stworzą folder *folder-docelowy*,
a następnie użyją ffmpeg do wycięcia ujęć i zapiszą je w nim w formacie
*(numer linii)\_(opis ujęcia).mp4*.

#### Sklejanie kadrów.

Do sklejania kadrów służy skrypt [run\_blender.sh](run_blender.sh) wywołujący
kopię kodu w pliku [make\_movie.py](make_movie.py) wewnątrz Blendera.

Zadaniem tego skryptu jest połączenie poszczególnych ujęć oraz
dodanie czołówki, tyłówki, paska z afiliacją i przejść.

Ścieżki do potrzebnych plików oraz parametry (typu długość
przejść, czas wyświetlania paska z afiliacją) konfiguruje
się w pliku [config.ini](config.ini).
Pomysł jest taki, żeby w sekcji *DEFAULT* wpisywać ustawienia dla większej
liczby filmów (np. omówienia z całego konkursu), a potem dodawać
sekcje dla poszczególnych zadań z ustawieniami per omówienie.
W takich sekcjach można też nadpisywać ustawienia w *DEFAULT*,
sposób parsowania tego pliku jest opisany
[tutaj](https://docs.python.org/3.5/library/configparser.html).

Należy ustawić odpowiednio ścieżki *CONFIG_FILE*, *BLENDER_EXEC*
i *BLENDER_FILE*
w pliku *run_blender.sh*,
a następnie wykonać
```
./run_blender.sh id
```
gdzie id jest nagłówkiem sekcji zawierającej odpowiednią konfigurację
w pliku config.ini.
Po jego wykonaniu otwiera się gotowy projekt Blendera z widokiem skonfigurowanym
do edycji wideo. Można oglądać go viewporcie, ewentualnie wprowadzać poprawki
w config.ini (kliknięcie *Run script* na nowo tworzy projekt z *config.ini*)
lub ręcznie (wymaga to pewnej znajomości Blendera). Kiedy projekt jest już
gotowy do renderowania, należy kliknąć przycisk *Animation* w panelu
*Properties* w prawym dolnym rogu.

#### Wskazówka na wszelki wypadek
Gdyby ktoś chciał modyfikować zawartość pliku *make_movie.py*, to
przyda się informacja, że skrypt *run_blender.sh* nie ładuje go z dysku,
ale korzysta z jego kopii włączonej w blenderowy plik *make_movie.blend*.
Żeby uzyskać jakieś nowe rezultaty, należy uaktualnić blok tekstowy 
*make_movie.py* w blenderowym edytorze tekstu.
