SERVICES=main
LIBS=protocol
UI=ui-mui

lint:
	for d in $(LIBS) $(SERVICES) $(UI); do make -C $$d lint; done

test:
	for d in $(LIBS) $(SERVICES) $(UI); do make -C $$d test; done
