all: css/jizera.min.css css/jizera.css

css/jizera.css: less/jizera.less less/frontpage.less less/general.less  less/grid.less less/placelist.less less/utils.less less/variables.less
	lessc $< > $@

css/jizera.min.css: css/jizera.css
	cleancss $< -o $@
