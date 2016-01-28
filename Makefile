test:
	py.test tests/
cov:
	py.test --cov=bottle_admin tests/
covgui: cov
	duvet
