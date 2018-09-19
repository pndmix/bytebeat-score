# bytebeat-score
This is a CLI *bytebeat* sound application with python3. Bytebeat is algorithmic sound generated from one line of code.

## Prerequisites
- numpy
- pyaudio

~~~bash
$ pip install -r requirements.txt
~~~

## Usage
### play simple quater notes
~~~bash
$ python bytebeat.py "t>>4"

Sampling rate: 8000 Hz, Playback time: 30 sec
~~~
**Note**: enclose bytebeat characters in double quotes (e.g. *"t>>4"*)

### play and score melody
~~~bash
$ python bytebeat.py "(t*((2+(t>>9&4))*(2+(3&t>>14))))>>(t>>8&2)" --score

Sampling rate: 8000 Hz, Playback time: 30 sec
Scoring now ... done.
~~~
Use score option, save this sound and a score file in [./scores](./scores) directory. More example sounds in [./scores/examples](./scores/examples) directory.  
**Note**: can be set the sound filename as score option's argument (e.g. *./scores/melody.wav*)

### optional features list
| option | feature |
| --- | --- |
| -h, --help | show this help message
| -r, --rate | set sampling rate[Hz]
| -t, --time | set playback time[seconds]
| -s, --score | write bytebeat sound in wav

## Reference
- Viznut's blog
  - [Algorithmic symphonies from one line of code -- how and why?](http://countercomplex.blogspot.com/2011/10/algorithmic-symphonies-from-one-line-of.html)
  - [Some deep analysis of one-line music programs.](http://countercomplex.blogspot.com/2011/10/some-deep-analysis-of-one-line-music.html)
- Kragen's text
  - [Bytebeat — Kragen](http://canonical.org/~kragen/bytebeat/)
