jsdir 	= ../static/js
cssdir 	= ../static/css
stylecss = compact

all: 	$(patsubst %,$(jsdir)/%.js,jizera landing) \
		$(patsubst %,$(cssdir)/%.css,style placelist landing grid)

VPATH = scss:coffee

grid.scss: _grid_core.scss

$(cssdir)/%.css: %.scss
	sass -C --sourcemap=none --style $(stylecss) $<:$@

$(jsdir)/%.js: %.coffee
	coffee -cbp $< > $@

clean:
	rm -rf *.map .sass-cache
