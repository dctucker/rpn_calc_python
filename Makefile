SRCDIR=../rpn_calc
OUTDIR=../rpn_calc_python
SOURCES=\
		$(wildcard $(SRCDIR)/src/*.php)\

TEST_SOURCES=\
		$(wildcard $(SRCDIR)/tests/*.php)\

all: python_tests python

python: $(SOURCES)
	@mkdir -p $(OUTDIR)/src
	@touch $(OUTDIR)/src/__init__.py
	@- $(foreach file,$^,ex $(file) < php2py.vim ;)


python_tests: $(TEST_SOURCES)
	@touch $(OUTDIR)/tests/__init__.py
	@- $(foreach file,$^,ex $(file) < php2py.vim ;)

json:
	#cp -R $(SRCDIR)/tests/json_responses $(OUTDIR)/tests/

install:
	#pip install mock requests redis responses python-dateutil


.ONESHELL:
test:
	@PYTHONPATH="$(OUTDIR)/src:$(OUTDIR)/tests" python -m unittest discover -s tests -p "*.py"
	#cd $(OUTDIR)/src ; python tests.py

clean:
	rm -f $(OUTDIR)/src/*.py

