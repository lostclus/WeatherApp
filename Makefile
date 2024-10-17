SERVICES=core.srv loader.srv query.srv
LIBS=protocol.lib
UI=ui

lint:
	for d in $(LIBS) $(SERVICES) $(UI); do make -C $$d lint; done

test:
	for d in $(LIBS) $(SERVICES) $(UI); do make -C $$d test; done
