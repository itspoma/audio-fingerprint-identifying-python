#  How to set up 

1. run `$ make clean reset` to clean & init database struct
1. copy `.mp3` audio files into `mp3/` directory
1. run `$ make fingerprint-songs` to analyze audio files
1. turn on any of audio files from `mp3/` directory, and run `$ make recognize-listen`

## Thanks to
- [How does Shazam work](http://coding-geek.com/how-shazam-works/)
- [Audio Fingerprinting with Python and Numpy](http://willdrevo.com/fingerprinting-and-audio-recognition-with-python/)
- [Shazam It! Music Recognition Algorithms, Fingerprinting, and Processing](https://www.toptal.com/algorithms/shazam-it-music-processing-fingerprinting-and-recognition)
- [Creating Shazam in Java](http://royvanrijn.com/blog/2010/06/creating-shazam-in-java/)