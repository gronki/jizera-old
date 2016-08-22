#!/bin/bash
set -e

lessc jizera.less css/jizera.css
lessc -x jizera.less css/jizera.min.css
