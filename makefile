all:
	cp main.py bchoc
	chmod +x bchoc

install:
	pip install -r requirements.txt

clean:
	rm -f blockchain.pkl
