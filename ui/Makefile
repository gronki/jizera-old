jsdir 	= ../jizera/static/js
cssdir 	= ../jizera/static/css
stylecss = compressed

all: 							\
		$(jsdir)/jizera.js		\
	 	$(jsdir)/landing.js 	\
		$(jsdir)/report.js 		\
		$(cssdir)/style.css 	\
		$(cssdir)/grid.css

VPATH = sass:coffee

$(cssdir)/grid.css: _respond.sass
$(cssdir)/style.css: 				\
			sass/_brightness.sass	\
			sass/_buttons.sass		\
			sass/_forms.sass		\
			sass/_landing.scss		\
			sass/_nav.sass			\
			sass/_tables.sass		\
			sass/_palette.sass		\
			sass/_placelist.scss	\
			sass/_respond.sass		\
			sass/_typography.sass


$(cssdir)/%.css: sass/%.sass
	sass --style $(stylecss) $<:$@

$(jsdir)/%.js: %.coffee
	coffee -cbp $< > $@

clean:
	rm -rf $(cssdir)/*.map .sass-cache
