$(document).ready ->
    $('input[type="checkbox"].toggle').change (e) ->
        tgt = $(this).attr('data-toggle')
        if $(this).prop('checked')
            $("##{tgt}").show()
        else
            $("##{tgt}").hide()
        return
    return
