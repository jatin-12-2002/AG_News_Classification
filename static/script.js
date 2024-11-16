document.getElementById("trainButton").addEventListener("click", async () => {
    try {
        const response = await fetch("/train");
        const { task_id } = await response.json();
        document.getElementById("trainingMessage").innerText = `Training started! Task ID: ${task_id}`;

        const statusInterval = setInterval(async () => {
            const statusResponse = await fetch(`/train-status/${task_id}`);
            const statusData = await statusResponse.json();

            if (statusData.status === "Success") {
                clearInterval(statusInterval);
                document.getElementById("trainingMessage").innerText = "Training completed successfully!";
            } else if (statusData.status === "Failure") {
                clearInterval(statusInterval);
                document.getElementById("trainingMessage").innerText = `Training failed: ${statusData.error}`;
            }
        }, 5000);
    } catch (error) {
        document.getElementById("trainingMessage").innerText = `Failed to start training. ${error.message}`;
    }
});

document.getElementById("predictButton").addEventListener("click", async () => {
    const textInput = document.getElementById("textInput").value; // Get text input value
    if (!textInput.trim()) {
        alert("Input text cannot be empty.");
        return;
    }

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: textInput }),
        });
        const { task_id } = await response.json();
        document.getElementById("output").style.display = "block";
        document.getElementById("label").innerText = "Prediction in progress...";
        document.getElementById("confidence").innerText = "";

        const statusInterval = setInterval(async () => {
            const statusResponse = await fetch(`/predict-status/${task_id}`);
            const statusData = await statusResponse.json();

            if (statusData.status === "Success") {
                clearInterval(statusInterval);
                document.getElementById("label").innerText = statusData.result.label;
                document.getElementById("confidence").innerText = statusData.result.confidence;
            } else if (statusData.status === "Failure") {
                clearInterval(statusInterval);
                document.getElementById("label").innerText = "Error occurred during prediction.";
                document.getElementById("confidence").innerText = "";
            }
        }, 5000);
    } catch (error) {
        alert(`Failed to start prediction. ${error.message}`);
    }
});