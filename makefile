all:
	cp main.py bchoc
	chmod +x bchoc
	rm -f BlockChain.bin
	clear
	./bchoc init
	./bchoc add -c e0587203-f3bd-408c-8fc2-227ab7883da9 -i 3436504811 -g H4ruUX9AfbWU -p C67C
	./bchoc checkout -i 3436504811 -p E69E

	
