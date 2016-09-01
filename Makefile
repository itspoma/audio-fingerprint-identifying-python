.PHONY: tests

install:
	@echo soon

clean:
	@find . -name \*.pyc -delete

tests:
	@python tests/*.py

stat:
	@python get-database-stat.py

reset:
	@python reset-database.py

fingerprint-songs: clean
	@python collect-fingerprints-of-songs.py

recognize-listen: clean
	@python recognize-from-microphone.py

recognize-file: clean
	@python recognize-from-file.py