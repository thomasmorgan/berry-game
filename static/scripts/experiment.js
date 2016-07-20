lock = true;
current_trial = 0;
dimensions = ["color", "shininess", "spottiness"];

insert_berry_number = function() {
    reqwest({
        url: "/experiment_property/num_trials",
        method: 'get',
        type: 'json',
        success: function (resp) {
            $("#n_berries").html(resp.num_trials);
        },
    });
};

start_trials = function() {
    reqwest({
        url: "/experiment_property/num_trials",
        method: 'get',
        type: 'json',
        success: function (resp) {
            blah = resp;
            num_berries = resp.num_trials;
            colors = [];
            shininesses = [];
            spottinesses = [];
            for (i = 0; i<num_berries; i++) {
                colors.push((Math.random() * 0.5 + 0.25).toFixed(2));
                shininesses.push((Math.random() * 0.5 + 0.25).toFixed(2));
                spottinesses.push((Math.random() * 0.5 + 0.25).toFixed(2));
            }
            create_agent();
        },
    });
};

// Create the agent.
create_agent = function() {
    reqwest({
        url: "/node/" + participant_id,
        method: 'post',
        type: 'json',
        success: function (resp) {
            my_node_id = resp.node.id;
            present_stimulus();
        },
        error: function (err) {
            console.log(err);
            err_response = JSON.parse(err.response);
            if (err_response.hasOwnProperty('html')) {
                $('body').html(err_response.html);
            } else {
                allow_exit();
                go_to_page('postquestionnaire');
            }
        }
    });
};

present_stimulus = function() {
    $("#title").css('visibility', 'hidden');
    $(".berry_div").css('visibility', 'hidden');
    $("#button_div").css('visibility', 'hidden');

    $("#trial_counter").html("This is trial " + (current_trial+1) + " of " + num_berries + ".");

    color = colors[current_trial];
    shininess = shininesses[current_trial];
    spottiness = spottinesses[current_trial];

    $("#red_body").css("opacity", color);
    $("#glint").css("opacity", shininess);
    $("#spots").css("opacity", spottiness);

    dimension = dimensions[Math.floor(Math.random()*3)];
    if (dimension == "color") {
        value = colors[current_trial];
        $("#title").html("Is this berry red or blue?");
        $("#left_button").html("Red");
        $("#right_button").html("Blue");
    } else if (dimension == "shininess") {
        value = shininesses[current_trial];
        $("#title").html("Is this berry shiny or dull?");
        $("#left_button").html("Shiny");
        $("#right_button").html("Dull");
    } else {
        value = spottinesses[current_trial];
        $("#title").html("Does this berry have bold spots or pale spots?");
        $("#left_button").html("Bold");
        $("#right_button").html("Pale");
    }
    setTimeout(show1, 500);
    setTimeout(show1b, 1500);
    setTimeout(show2, 2500);
};

show1b = function() {
    $(".berry_div").css('visibility', 'visible');
};

show1 = function() {
    $("#title").css('visibility', 'visible');
};

show2 = function() {
    $("#button_div").css('visibility', 'visible');
    lock = false;
};

$(document).keydown(function(e) {
    var code = e.keyCode || e.which;
    if (code == 37) {
        left_click();
    } else if (code == 39) {
        right_click();
    }
});

left_click = function() {
    if (lock === false) {
        right = value > 0.5;
        lock = true;
        if (dimension == "color") {
            submit_response("red");
        } else if (dimension == "shininess") {
            submit_response("shiny");
        } else {
            submit_response("bold");
        }
    }
};

right_click = function() {
    if (lock === false) {
        right = value < 0.5;
        lock = true;
        if (dimension == "color") {
            submit_response("blue");
        } else if (dimension == "shininess") {
            submit_response("dull");
        } else {
            submit_response("pale");
        }
    }
};

submit_response = function(response) {
    reqwest({
        url: "/info/" + my_node_id,
        method: 'post',
        data: {
            contents: response,
            info_type: "Decision",
            property1: dimension,
            property2: current_trial,
            property3: value,
            property4: [color, shininess, spottiness].toString(),
            property5: right
        },
        success: function (resp) {
            current_trial += 1;
            if (current_trial<num_berries) {
                present_stimulus();
            } else {
                allow_exit();
                go_to_page('postquestionnaire');
            }
        }
    });
};
