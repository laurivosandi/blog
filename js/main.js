$(document).ready(function() {
    if ($("#search")) {
        $("#search").on("keyup", function(e) {
            e.preventDefault();
            var key = e.keyCode || e.which;
            if (key != 13) { return; }
            var query = $("#search").val();
            if (query.length < 3) { return; }
            query = encodeURIComponent(query);
            if (query == window.location.hash) { return; }
            window.location = "/search.html#" + query;
        });

        if (window.location.pathname != "/search.html") { return; }

        $("#search").focus();
        
        $(window).bind( 'hashchange', function(e) {
            var query = window.location.hash.substring(1);
            $(".document.search h1").html("Search results for " + query);
            var normalized = "|" + query.toLowerCase() + "|";
            $("#content .resource").each(function(index) {
                if (normalized.length < 3 || $(this).attr("data-keywords").indexOf(normalized) >= 0) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            });
        });
  
        $("#search").val(window.location.hash.substring(1));

        if (window.location.pathname == "/search.html") {
            $(window).trigger("hashchange");
        }
    }
});
