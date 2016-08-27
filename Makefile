install:
	@echo soon

clean:
	@find . -name \*.pyc -delete

parse: clean
	@python parse-songs-and-collect-hashes.py

recognize-listen: clean
	@python recognize-from-microphone.py

recognize-file: clean
	@python recognize-from-file.py