var ledBtnColours = {
    btnR:"btn-danger",
    btnG:"btn-success",
    btnB:"btn-primary",
    btnW:"btn-light",
    btnIR:"btn-secondary"
};

function updateLedStatus(ledBtn, isOn) {
    ledBtn.className = "btn " + (isOn ? ledBtnColours[ledBtn.id] : "btn-dark");
}

function toggleLed() {
    var btn = this;
    var isOn = !btn.classList.contains("btn-dark");

    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/leds/"+this.id.slice(3)+"/set?on="+(!isOn));
    xhttp.responseType = "json";
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            updateLedStatus(btn, this.response.isOn);
        }
    };
    xhttp.send();

    btn.blur();  // Removes focus from the button
}

Object.keys(ledBtnColours).forEach(function(id) {
    // Attach the toggle function to each button to toggle the LEDs
    var btn = document.getElementById(id);
    btn.addEventListener("click", toggleLed);

    // Initialise the buttons with the current LED states
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/leds/"+id.slice(3)+"/isOn");
    xhttp.responseType = "json";
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            updateLedStatus(btn, this.response.isOn);
        }
    };
    xhttp.send();
});
