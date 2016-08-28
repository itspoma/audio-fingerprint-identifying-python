install:
	@echo soon

clean:
	@find . -name \*.pyc -delete

fingerprint-songs: clean
	@python collect-fingerprints-of-songs.py
	@python get-database-stat.py

recognize-listen: clean
	@python recognize-from-microphone.py

recognize-file: clean
	@python recognize-from-file.py