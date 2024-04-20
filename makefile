all:
	cp main.py bchoc
	chmod +x bchoc
	rm -f BlockChain.bin
	clear
	./bchoc init
	./bchoc add -c abd7d92f-cd5b-4076-86e3-ef8bae6634bc -i 2307677060 -g knwaGcuR2RUa -p C67C
	./bchoc checkout -i 2307677060 -p L76L
	./bchoc checkin -i 2307677060 -p E69E

	
