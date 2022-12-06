run:
	python main.py --data filmtrust --method IBSO --size 128

setup: requirements.txt
	pip install -r requirements.txt

clean:
	rm -rf __pycache__