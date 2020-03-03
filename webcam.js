var video = document.querySelector("#videoElement");
console.log(video)
function start(){
    console.log("start")
    
    navigator.mediaDevices.getUserMedia({video: true, audio: false})
    .then(function(stream) {
        console.log('fail')
        video.srcObject = stream;
        console.log('pass')
        video.play();
    })
    .catch(function(err) {
        console.log("An error occurred: " + err);
    });
}

function stop() {
    console.log("stop");
    var stream = video.srcObject;
    var tracks = stream.getTracks();

    for (var i = 0; i < tracks.length; i++) {
        var track = tracks[i];
        track.stop();
    }

    video.srcObject = null;
}
