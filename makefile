all: copy_main make_executable

copy_main:
	cp main.py bchoc

make_executable:
	chmod +x main.py
