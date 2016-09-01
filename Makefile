.PHONY: tests

install:
	@echo soon

clean:
	@find . -name \*.pyc -delete

reset:
	@python reset-database.py

tests:
	@python tests/*.py

stat:
	@python get-database-stat.py

fingerprint-songs: clean
	@python collect-fingerprints-of-songs.py

recognize-listen: clean
	@python recognize-from-microphone.py -s $(seconds)

recognize-file: clean
	@python recognize-from-file.py