// Initialize TensorFlow.js and the FaceMesh model
async function initialize() {
    const video = document.getElementById('video');
    const status = document.getElementById('status');

    // Access webcam
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;

    // Load the FaceMesh model
    const model = await facemesh.load();
    status.textContent = 'Model loaded, detecting faces...';

    // Continuously process the video feed
    const detectFace = async () => {
        const predictions = await model.estimateFaces(video, false);
        if (predictions.length > 0) {
            status.textContent = 'Face detected!';
            // Send face detection status to the backend
            const response = await fetch('http://localhost:5000/secure', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ action: 'authenticate', data: 'face_detected' })
            });
            const result = await response.json();
            console.log(result);
        } else {
            status.textContent = 'No face detected.';
        }
        requestAnimationFrame(detectFace);
    };

    detectFace();
}

initialize();
