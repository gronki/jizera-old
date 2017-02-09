jsdir 	= ../static/js
cssdir 	= ../static/css
stylecss = compressed

all: 	$(jsdir)/jizera.js $(jsdir)/landing.js \
		$(cssdir)/light.css \
		$(cssdir)/grid.css

VPATH = scss:coffee

$(cssdir)/grid.css: _respond.scss
$(cssdir)/light.css: _style_core.scss _buttons.scss _forms.scss _landing.scss _nav.scss _placelist.scss _respond.scss _text-and-backgrounds.scss

$(cssdir)/%.css: scss/%.scss
	sass --style $(stylecss) $<:$@

$(jsdir)/%.js: %.coffee
	coffee -cbp $< > $@

clean:
	rm -rf $(cssdir)/*.map .sass-cache
