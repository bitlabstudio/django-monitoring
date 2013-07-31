function load_monitor(container) {
    url = $(container).attr('data-url');
    get_data = {};
    $.get(url, get_data, function(data, textStatus, jqXHR) {
        $(container).html(data);
    });
}

$(document).ready(function() {
    $('.monitorContainer').each(function() {
        load_monitor(this);
    });
});
