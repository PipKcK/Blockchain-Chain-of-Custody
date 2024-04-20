all:
	cp main.py bchoc
	chmod +x bchoc
	rm -f BlockChain.bin
	clear
	./bchoc init
	./bchoc add -c 77f50a62-d198-43a1-81ac-dffbff88308a -i 2775647613 -i 3668088400 -i 2392419778 -i 3402671448 -i 2758133383 -g GoWlApWMnBSY -p C67C
	
