function play(bpm, timeSignature, onSuccess) {
    $.ajax({
        url: "play_drums",
        data: {
            bpm: bpm,
            time_signature: timeSignature
        },
        dataType: "json",
        type: "GET",
        success: function(response) {
            onSuccess(response);
        }
    });
}

$("#play-drums").on("click", function() {
    let bpm = $("#bpm").val();
    let timeSignature = $("#time-signature").val();
    play(bpm, timeSignature, function(message) {
        $("#message").text(message);
    });
});

