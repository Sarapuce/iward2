function toggleDebug() {
    var debugText = document.getElementById("debug-text");

    if (debugText.style.display === "none") {
        debugText.style.display = "block";
    } else {
        debugText.style.display = "none";
    }
}