all:
	cp main.py bchoc
	chmod +x bchoc
	rm -f BlockChain.bin
	clear
	./bchoc init
	./bchoc add -c d2a5c64b-b0e9-46cc-8703-41e4f4f804f5 -i 1938779513 -g hnTP5u5biPDH -p C67C
	./bchoc checkout -i 1938779513 -p E69E


	
