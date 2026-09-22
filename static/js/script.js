const objectCount = document.getElementById("object-count");
const inCount = document.getElementById("in-count");
const outCount = document.getElementById("out-count");
const systemStatus = document.getElementById("system-status");

const classList = document.getElementById("class-list");


// Video upload elements

const uploadForm = document.getElementById("upload-form");
const videoFile = document.getElementById("video-file");
const videoFeed = document.getElementById("video-feed");


// Update dashboard statistics

function updateStatus() {

    fetch("/api/status")

        .then(response => response.json())

        .then(data => {

            objectCount.textContent = data.objects;

            inCount.textContent = data.in;

            outCount.textContent = data.out;

            systemStatus.textContent = data.status;


            classList.innerHTML = "";


            for (const className in data.classes) {

                const classItem = document.createElement("div");

                classItem.className = "class-item";


                classItem.innerHTML = `
                    <span>${className}</span>
                    <span>${data.classes[className]}</span>
                `;


                classList.appendChild(classItem);

            }

        })

        .catch(error => {

            console.error("Status error:", error);

        });

}


// Handle video upload

uploadForm.addEventListener("submit", function(event) {

    event.preventDefault();


    const file = videoFile.files[0];


    if (!file) {

        alert("Please select a video first.");

        return;

    }


    const formData = new FormData();

    formData.append("video", file);


    systemStatus.textContent = "UPLOADING";


    fetch("/upload", {

        method: "POST",

        body: formData

    })

    .then(response => response.json())

    .then(data => {

        if (data.error) {

            alert(data.error);

            systemStatus.textContent = "ERROR";

            return;

        }


        console.log(data.message);


        systemStatus.textContent = "STARTING";


        // Start the uploaded video

        videoFeed.src = "/api/video?" + new Date().getTime();

    })

    .catch(error => {

        console.error("Upload error:", error);

        systemStatus.textContent = "ERROR";

    });

});


// Update dashboard every second

updateStatus();

setInterval(updateStatus, 1000);