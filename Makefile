all:
	cp main.py bchoc
	chmod +x bchoc

clean:
	rm -f bchoc
	rm -f $(BCHOC_FILE_PATH)

install:
	pip install -r requirements.txt

view-path:
	echo $$BCHOC_FILE_PATH

test:
	./bchoc init
	./bchoc add -c f091d6fa-341d-4580-b283-8a5c08807c68 -i 1445825130 -g Ngyd4a8V8zMs -p C67C
	./bchoc checkout -i 1445825130 -p E69E
	./bchoc checkin -i 1445825130 -p A65A
	./bchoc show history -i 1445825130

