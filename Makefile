# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

theme_sources = $(wildcard sphinxext/zbtheme/*.html) sphinxext/zbtheme/support.py

sphinxext/zbtheme/static/zb.css: sphinxext/zbtheme/css/zb.in.css $(wildcard sphinxext/zbtheme/css/*.css) $(theme_sources)
	woosh -o $@ $(addprefix --source=,$(theme_sources)) $<

css: sphinxext/zbtheme/static/zb.css

html: sphinxext/zbtheme/static/zb.css
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	rm -f sphinxext/zbtheme/static/zb.css
	@$(SPHINXBUILD) -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

install-woosh:
	go install zombiezen.com/go/woosh/cmd/woosh@7dafeacc239d9379afa062b6e4a0e0bcfefc26c1

.PHONY: help css clean html install-woosh sphinxext/zbtheme/support.py Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

%.css:
%.html:
