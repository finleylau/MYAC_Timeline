$(function () {
    // execute when DOM is fully loaded

    // initial message
    document.getElementById("year-title").innerHTML = "<h2>Click on a year to get started!</h2>";

    // make navbar
    var navbar = document.getElementById("timeline-navbar");

    var navbarHTML = "";

    $.getJSON(Flask.url_for("year_info"), function (data) {
        if (data != null) {
            $.each(data, function (key, value) {
                // update navbar HTML
                console.log(key)
                console.log(value.year_info.start_year)
                navbarHTML = "<li><a href='" + Flask.url_for("error") + "' onclick='renderYear(" + key + "); return false; '>" +
                    value.year_info.start_year + "-" + value.year_info.end_year + "</a></li>" + navbarHTML;
            });
        }
        navbar.innerHTML = navbarHTML;
    });

    // When the user scrolls down 20px from the top of the document, show the button
    window.onscroll = function () { scrollFunction() };
    
})

// scroll to top function
function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("topbutton").style.display = "block";
    } else {
        document.getElementById("topbutton").style.display = "none";
    }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

// render year data
function renderYear(year_id) {

    // format input
    var year_ID = parseInt(year_id);

    // get elements
    var title = document.getElementById("year-title");
    var events = document.getElementById("year-events");
    var board = document.getElementById("board");
    var artistic = document.getElementById("artistic");
    var admin = document.getElementById("admin");

    // initialize html variables
    var titlehtml = "";
    var eventshtml = "";
    var boardhtml = "<h5>Board of Directors</h5><hr />";
    var artistichtml = "<h5>Artistic Faculty</h5><hr />";
    var adminhtml = "<h5>Administrative Staff</h5><hr />";

    $.getJSON(Flask.url_for("year_info"), function (data) {
        if (data != null) {
            // loop over years for the year with the right key
            $.each(data, function (key, value) {
                var key_id = parseInt(key);
                if (key_id == year_ID) {

                    // update year title
                    titlehtml = titlehtml + "<h2>" + value.year_info.start_year + "-" + value.year_info.end_year + "</h2>"

                    // loop through the events
                    $.each(value.events, function (index) {
                        var p = "<p>";
                        var endp = "</p>";
                        eventshtml = eventshtml + "<div class='row event'>" + "<div class='col-sm-6'>" + "<h6 class='event-title'>";
                        var eventdate = " - (" + value.events[index].month + "/" + value.events[index].day + ")";
                        eventshtml = eventshtml + value.events[index].name + eventdate + "</h6>";
                        var description = "";
                        if (value.events[index].description != "None") {
                            description = p + value.events[index].description + endp;
                        }
                        var link = "";
                        if (value.events[index].link != "") {
                            link = p + "<a target='_blank' href='" + value.events[index].link + "'>Video Link</a>" + endp;
                        }
                        var media = "";
                        if (value.events[index].media_path != "") {
                            media = p + "<a target='_blank' href='/" + value.events[index].media_path + "'>Media File</a>" + endp;
                        }
                        eventshtml = eventshtml + description + link + media + "</div>";
                        var image = "";
                        if (value.events[index].image_path != "") {
                            image = "<div class='col-sm-6'><img src='" + value.events[index].image_path + "' alt='' /></div>";
                        }
                        eventshtml = eventshtml + image + "</div>";
                    });
                    // loop through the people
                    $.each(value.people.board, function (index) {
                        boardhtml = boardhtml + "<p>" + value.people.board[index] + "</p>";
                    });
                    $.each(value.people.artistic, function (index) {
                        artistichtml = artistichtml + "<p>" + value.people.artistic[index] + "</p>";
                    });
                    $.each(value.people.admin, function (index) {
                        adminhtml = adminhtml + "<p>" + value.people.admin[index] + "</p>";
                    });
                }
            });
        }

        // update html
        title.innerHTML = titlehtml;
        events.innerHTML = eventshtml;
        board.innerHTML = boardhtml;
        artistic.innerHTML = artistichtml;
        admin.innerHTML = adminhtml;
    })
}