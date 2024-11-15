document.getElementById("predictButton").addEventListener("click", async () => {
    const inputText = document.getElementById("inputText").value.trim();

    if (!inputText) {
        alert("Please enter some text to predict.");
        return;
    }

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ text: inputText }),
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const result = await response.json();
        document.getElementById("category").textContent = result.label;
        document.getElementById("confidence").textContent = `${(result.confidence * 100).toFixed(2)}%`;
        document.getElementById("output").style.display = "block";
    } catch (error) {
        alert(`Failed to fetch prediction. ${error.message}`);
    }
});

document.getElementById("trainButton").addEventListener("click", async () => {
    try {
        const response = await fetch("/train", { method: "GET" });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        alert("Model training started successfully. Please wait until it completes.");
    } catch (error) {
        alert(`Failed to start training. ${error.message}`);
    }
});