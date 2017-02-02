jsdir 	= ../static/js
cssdir 	= ../static/css
stylecss = compact

all: 	$(jsdir)/jizera.js $(jsdir)/landing.js \
		$(cssdir)/dark.css \
		$(cssdir)/light.css \
		$(cssdir)/night.css \
		$(cssdir)/grid.css

VPATH = scss:coffee

$(cssdir)/%.css: scss/%.scss $(wildcard scss/_*.scss)
	sass -C --sourcemap=none --style $(stylecss) $<:$@

$(jsdir)/%.js: %.coffee
	coffee -cbp $< > $@

clean:
	rm -rf *.map .sass-cache
