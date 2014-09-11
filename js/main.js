function createBreadcrumbs() {
    window.PATH = decodeURIComponent(window.location.pathname);
    if (window.location.protocol == "file:" && window.location.pathname.indexOf("/home/") == 0) {
        window.PATH = decodeURIComponent("/~" + window.location.pathname.substring(6));
    }
    window.PATH_COMPONENTS = window.location.pathname == "/" ? [] : window.PATH.replace(/^\/+|\/+$/g, '').split("/");

    /* Generate navigation bar on the fly */
    var $nav = $("#breadcrumbs");
    $nav.empty();
    if (window.location.host) {
        var internationalized_domain_name = window.location.host.split(".").map(function(j) { return j.indexOf("xn--") == 0 ? punycode.decode(j.substring(4)) : j;}).join(".");
        $nav.prepend("<a class=\"root\" href=\"" + window.location.origin + "\">" + internationalized_domain_name + "</a>");
    }
    var title = null;
    var hadHome = false; // Whether we already included home folder in the breadcrumbs
    
    for (var j = 0; j < window.PATH_COMPONENTS.length - 1; j++) {
        title = window.PATH_COMPONENTS[j];
        var url = encodeURI("/" + window.PATH_COMPONENTS.slice(0, j+1).join("/") + "/");
        if (!hadHome && title[0] == '~') {
            $nav.append("<a class=\"directory item home\" href=\"" + url + "\">" + title.substring(1) + "</a>");
            hadHome = true;
        } else {
            $nav.append("<a class=\"directory item\" href=\"" + url + "\">" + title + "</a>");
        }
    }
    $nav.append("<a class=\"page\" href=\"#\">" + $("head title").html() + "</a>");
}

$(document).ready(function() {

    $("#sidebar").append($("<section id=\"location\"></section>"));
    $("#location").append("<a class=\"icon qr\" href=\"http://qrf.in/?url=" + window.location.href + "\">Shorten URL</a>");
    
    $(document).ready(function() {

        if ($("#search")) {
            $("#search").on("search", function(e) {
                var query = $("#search").val();
                window.location = "/search.html#" + query;
            });
            
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
                
/*                $("#content .archive").each(function(e) {
                    console.log("Checking:", this);
                    console.log($(".post", this));
                    if ($(".post:hidden", this).size() != $(".post", this).size()) { // This is the wurst!
                        $("h1", this).show();
                    } else {
                        $("h1", this).hide();
                    }
                });*/
            });
      
            $("#search").val(window.location.hash.substring(1));

            if (window.location.pathname == "/search.html") {
                $(window).trigger("hashchange");
            }

        }
    });
/*    $("table.docutils.footnote").each(function(e) {
        $("#document").append($(this).remove());
    });*/
    
/*    if ($("#content .document")) {
        var published = new Date($("head meta[name=published]").attr("content"));
        var published = ["Jan", published.getMonth() + " '" + (published.getYear() - 100)
        $("#content .document h1").first().append("<span class=\"published\">" + published + "</span>");
    }*/



});
