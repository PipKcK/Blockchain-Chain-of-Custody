all:
	cp main.py bchoc
	chmod +x bchoc
	rm -f BlockChain.bin
	clear
	./bchoc init
	./bchoc add -c 93a3e215-5b71-4175-8411-d9374cc3e663 -i 2608608139 -i 3796006652 -i 2539237045 -i 1875275885 -i 349322093 -i 649233882 -g P9PhI6UttXc1 -p C67C

	
