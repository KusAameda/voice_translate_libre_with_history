function startRecording() {
    const recognition = new webkitSpeechRecognition();
    recognition.lang = 'ja-JP';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = function(event) {
        const text = event.results[0][0].transcript;
        document.getElementById('input-text').innerText = text;

        fetch('/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('output-text').innerText = data.translated;
        });
    };

    recognition.onerror = function(event) {
        alert('Error occurred: ' + event.error);
    };

    recognition.start();
}
