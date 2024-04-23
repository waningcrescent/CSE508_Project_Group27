document.getElementById('processBtn').addEventListener('click', function() {
    var inputText = document.getElementById('inputText').value;
    document.getElementById('outputText').value = "Processing...";
  
    fetch('/process-input', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: inputText })
    })
    .then(response => {
        // Check if the response is ok (status 200)
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        // Display the output or an error message
        if (data.output) {
            document.getElementById('outputText').value = data.output;
        } else if (data.error) {
            document.getElementById('outputText').value = data.error;
        }
    })
    .catch(error => {
        // Catch any errors and display them
        console.error('Error:', error);
        document.getElementById('outputText').value = "Error processing the text. Check the console for more details.";
    });
  });
  