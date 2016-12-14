deps = $(wildcard jizera/*.scss)

jsdir 	= ../static/js
cssdir 	= ../static/css

alljs 	= jizera jizera.front
allcss 	= jizera jizera.front

SASSFLAGS ?= -C --sourcemap=none

all: 	$(patsubst %,$(jsdir)/%.js,$(alljs)) \
		$(patsubst %,$(cssdir)/%.css,$(allcss))

$(cssdir)/%.css: %.scss $(deps)
	sass $(SASSFLAGS) --style compact $<:$@

$(cssdir)/%.min.css: %.scss $(deps)
	sass $(SASSFLAGS) --style compressed $<:$@

$(jsdir)/%.js: %.coffee
	coffee -cbp $(COFFEEFLAGS) $< > $@

clean:
	rm -rf *.map .sass-cache
