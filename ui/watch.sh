#!/bin/bash

# set -e

################################################################################
################################################################################

FN=$(ls less/*)
CMD="lessc less/jizera.less less/jizera.css
lessc -x less/jizera.less css/jizera.min.css"

################################################################################
################################################################################

function get_timestamps {
    local FNLIST=$1
    local TSLIST=""
    for  i in $FNLIST
    do
        TSLIST="$TSLIST $(stat -c %Z $i)"
    done
    echo $TSLIST
}

LTIME=$(get_timestamps "$FN")


while true
do
   ATIME=$(get_timestamps "$FN")

   if [[ "$ATIME" != "$LTIME" ]]
   then
        clear
        echo ""
        echo ""
        echo "===================================================================="
        echo "===================================================================="
        echo ""
        #############


bash <<EOF
        set -e
        $CMD
EOF


        ################
        LTIME=$ATIME
   fi
   sleep 0.5
done
