
latlng2str = (latlng) ->
    latstr = parseFloat(latlng.lat()).toFixed(6)
    lngstr = parseFloat(latlng.lng()).toFixed(6)
    "#{latstr}, #{lngstr}"

latlng2strgmap = (latlng) ->
    latstr = parseFloat(latlng.lat).toFixed(6)
    lngstr = parseFloat(latlng.lng).toFixed(6)
    "#{latstr}, #{lngstr}"

str2latlngs = (s) -> -1

run_geolocation = (handler,handler_error) ->
    loc_timeout = 10
    geolatlng = null
    if navigator.geolocation
        navigator.geolocation.getCurrentPosition (position) ->
            geolatlng = { lat:position.coords.latitude, lng:position.coords.longitude}
            handler geolatlng
        , (e) ->
            if typeof handler_error is "function" then handler_error
        , {timeout:loc_timeout*1000,enableHighAccuracy:true,maximumAge:120*1000}
    else
        if typeof handler_error is "function" then handler_error
