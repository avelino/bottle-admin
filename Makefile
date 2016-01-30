test:
	py.test tests/
cov:
	py.test --cov=bottle_admin tests/
covgui: cov
	duvet
clean:
	find bottle_admin/ tests/ -name *.pyc | xargs rm
