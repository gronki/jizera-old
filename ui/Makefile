jsdir 	= ../jizera/static/js
cssdir 	= ../jizera/static/css
stylecss = compressed

all: 	$(jsdir)/jizera.js\
	 	$(jsdir)/landing.js \
		$(jsdir)/report.js \
		$(cssdir)/style.css \
		$(cssdir)/grid.css

VPATH = sass:coffee

$(cssdir)/grid.css: _respond.sass
$(cssdir)/style.css: _brightness.sass _buttons.sass _forms.sass _landing.scss _nav.sass _palette.sass _placelist.scss _respond.sass

$(cssdir)/%.css: sass/%.sass
	sass --style $(stylecss) $<:$@

$(jsdir)/%.js: %.coffee
	coffee -cbp $< > $@

clean:
	rm -rf $(cssdir)/*.map .sass-cache
