install:
	@echo soon

clean:
	@find . -name \*.pyc -delete

parse-songs: clean
	@python collect-fingerprints-of-songs.py

recognize-listen: clean
	@python recognize-from-microphone.py

recognize-file: clean
	@python recognize-from-file.py