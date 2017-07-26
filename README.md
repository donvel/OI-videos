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
*`(numer linii)\_(opis ujęcia).mp4*.

#### Wycinanie kardów

ad
