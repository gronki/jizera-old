jsdir 	= ../static/js
cssdir 	= ../static/css
stylecss = expanded

all: 	$(jsdir)/jizera.js $(jsdir)/landing.js \
		$(cssdir)/light.css \
		$(cssdir)/grid.css

VPATH = scss:coffee

$(cssdir)/grid.css: scss/grid.scss scss/_respond.scss
	sass -C --sourcemap=none --style $(stylecss) $<:$@

$(cssdir)/%.css: scss/%.scss $(wildcard scss/_*.scss)
	sass -C --sourcemap=none --style $(stylecss) $<:$@

$(jsdir)/%.js: %.coffee
	coffee -cbp $< > $@

clean:
	rm -rf *.map .sass-cache
