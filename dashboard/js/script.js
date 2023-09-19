
async function load_elements(session_id) {
    try {
        results_div = document.getElementById("results");
        date_html = document.getElementById("datetime");
        env_html = document.getElementById("env");
        service_html = document.getElementById("service");
        total_html = document.getElementById("total");
        success_rate_html = document.getElementById("success_rate");

        const response = await fetch("/data/saved/" + session_id + ".json");
        const session = await response.json();
        var total_success = 0;

        results_div.innerHTML = "";
        for (let x = 0; x < session.length; x++) {
            $.get( "./js/files/result.html", function( data ) {
                data = data.replace('{title}', session[x].title);

                data = data.replaceAll('{url}', session[x].request);

                if (session[x].status) {
                    data = data.replace('{status-color}', "green");
                    data = data.replace('{status}', "Success");

                    data = data.replace('{errors}', "<li>No errors in this test</li>");
                    total_success++;
                } else {
                    data = data.replace('{status-color}', "red");
                    data = data.replace('{status}', "Failure");

                    var errors = ""
                    for (y = 0; y < session[x].errors.length; y++) {
                        errors += "<li>" + session[x].errors[y] + "</li>";
                    }

                    data = data.replace('{errors}', errors);
                }

                results_div.innerHTML += data;
                date_html.innerHTML = session[0].datetime;
                env_html.innerHTML = session[0].env;
                service_html.innerHTML = session[0].service;
                total_html.innerHTML = session.length;

                var width = 1;
                var id = setInterval(frame, 10);
                function frame() {
                    if (width >= (total_success/session.length)*100) {
                        clearInterval(id);
                    } else {
                        width++;
                        success_rate_html.style.width = width + '%';
                        success_rate_html.innerHTML =  width + '%';
                    }
                }
//                success_rate_html.style = "width:" + (total_success/session.length)*100 + "%;";
//                success_rate_html.innerHTML = (total_success/session.length)*100 + "%";
            });
        }
    } catch (error) {
        console.log(error)
        results_div.innerHTML = '<h2 class="css-text-grey css-padding-16"><i class="fa fa-warning fa-fw css-margin-right css-xxlarge css-text-teal"></i>Session ID does not exist :(</h2>';
        date_html.innerHTML = "N.A";
        env_html.innerHTML = "N.A";
        service_html.innerHTML = "N.A";
        total_html.innerHTML = "0";
        success_rate_html.style = "width:100%;";
        success_rate_html.innerHTML = "N.A";
    }
}

function collapse_errors(element) {
    element.classList.toggle("active");
    var content = element.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
}
