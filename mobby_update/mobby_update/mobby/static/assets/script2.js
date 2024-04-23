document.getElementById('processBtn').addEventListener('click', function() {
    var formData = new FormData(); // Create a FormData object

    // Check if input text is provided
    var inputText = document.getElementById('inputText').value.trim();
    if (inputText !== '') {
        formData.append('inputText', inputText);
    }

    // Check if a file input is provided
    var fileInput = document.getElementById('file-upload');
    if (fileInput.files.length > 0) {
        var file = fileInput.files[0];
        if (file) {
            formData.append('file', file);
        }
    }

    // Append other form data to the FormData object
    formData.append('summary_length', document.getElementById('summary_length').value);
    formData.append('language', document.getElementById('languageSelect').value);

    // Send the form data using fetch
    fetch('/process-input', {
        method: 'POST',
        body: formData // Pass the FormData object as the body
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        if (data.output) {
            document.getElementById('outputText').value = data.output;
        } else if (data.error) {
            document.getElementById('outputText').value = data.error;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('outputText').value = "Error processing the text. Check the console for more details.";
    });
});