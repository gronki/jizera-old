function latlng2str(latlng) {
    return ""+parseFloat(latlng.lat()).toFixed(6)+", "+parseFloat(latlng.lng()).toFixed(6);
}
function latlngs2str(latlng) {
    return ""+parseFloat(latlng.lat).toFixed(6)+", "+parseFloat(latlng.lng).toFixed(6);
}
function latlngs2strgmap(latlng) {
    return ""+parseFloat(latlng.lat).toFixed(6)+","+parseFloat(latlng.lng).toFixed(6);
}

function str2latlngs(str) {
    return -1;
}

function run_geolocation(handler,handler_error) {
    var geolatlng;
    var loc_timeout = 10;
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            geolatlng = { lat:position.coords.latitude, lng:position.coords.longitude};
            handler(geolatlng);
        }, function(e) {
            if (typeof handler_error === "function")   handler_error();
        }, {timeout:loc_timeout*1000,enableHighAccuracy:true,maximumAge:120*1000});
    } else {
        if (typeof handler_error === "function") handler_error();
    }
}

function scriptFrontPage() {
    $(document).ready(function(){
        run_geolocation(function(ll){
            $('#fp-search-geoloc [name=lat]').val(ll.lat);
            $('#fp-search-geoloc [name=lng]').val(ll.lng);
            $('.geoloc-depend').show();
            $('span.geoloc-depend').css('display','inline');
        });
    });
}
