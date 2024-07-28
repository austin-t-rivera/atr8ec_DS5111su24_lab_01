default:
	@cat makefile

get_texts:
	/bin/bash /home/ubuntu/atr8ec_DS5111su24_lab_01/get_the_books.sh

raven_line_count:
	@echo "'The Raven' line count:"
	@cat pg17192.txt | wc -l

raven_word_count:
	@echo "'The Raven' word count:"
	@cat pg17192.txt | wc -w

raven_counts:
	@echo "Lowercase 'raven' line count:"
	@cat pg17192.txt | grep 'raven' | wc -l

	@echo "Titlecase 'Raven' line count:"
	@cat pg17192.txt | grep 'Raven' | wc -l

	@echo "Ignored Case 'raven' line count:"
	@cat pg17192.txt | grep -i 'raven' | wc -l

total_lines:
	@echo "Total lines across all txt files:"
	@cat *.txt | wc -l

total_words:
	@echo "Total words across all txt files:"
	@cat *.txt | wc -w

setup:
	python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt
