
async function load_elements(session_id) {
    try {
        const response = await fetch("../data/saved/" + session_id + ".json");
        const session = await response.json();
        var total_success = 0;

        $results_div.html('');
        for (let x = 0; x < session.length; x++) {
            // use id with jquery
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
                        errors += "<li>" + html_encode(session[x].errors[y]) + "</li>";
                    }

                    data = data.replace('{errors}', errors);
                }

                $results_div.append(data);
                $date_html.html(session[0].datetime);
                $env_html.html(session[0].env);
                $service_html.html(session[0].service);
                $total_html.html(session.length);

                var width = 100;
                var id = setInterval(frame, 10);
                function frame() {
                    if (width <= (total_success/session.length)*100) {
                        $success_rate_html.html(width + '%');
                        clearInterval(id);
                    } else {
                        width--;
                        $success_rate_html.css("width", width + '%');
                        $success_rate_html.html(width + '%');
                    }
                }
            });
        }
    } catch (error) {
        console.log(session_id);
        if (session_id == "") {
            $results_div.html($('<div></div>', {
                class: 'css-middleleft',
                html: $('<h2></h2>', {
                    class: 'css-text-grey css-padding-16',
                    html: '<i class="fa fa-arrow-left fa-fw css-margin-right css-xxlarge css-text-teal"></i>Put your session ID here'
                })
            }))
        } else {
            $results_div.html($('<h2></h2>', {
                class: 'css-text-grey css-padding-16',
                html: '<i class="fa fa-warning fa-fw css-margin-right css-xxlarge css-text-teal"></i>Session ID does not exist :('
            }))
        }
        $date_html.html("N.A");
        $env_html.html("N.A");
        $service_html.html("N.A");
        $total_html.html("0");
        $success_rate_html.css("width", "100%");
        $success_rate_html.html("N.A");
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

function html_encode(s) {
  var el = document.createElement("div");
  el.innerText = el.textContent = s;
  s = el.innerHTML;
  return s;
}

function display_session_id(nbr) {
    var files = fs.readdirSync('./');
    console.log(files);
}
