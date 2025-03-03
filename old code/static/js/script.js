document.addEventListener('DOMContentLoaded', function () {
    // Fetch session data from the API
    fetch('/api/generate_session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            // Add any necessary parameters here
            themes: ['empty', 'submission'],
            duration: 15,
            difficulty: 'MODERATE',
            dominant_name: 'Master',
            subject_name: 'Slave',
            sub_pov: '1PS',
            dom_pov: '2PS'
        })
    })
    .then(response => response.json())
    .then(data => {
        const lines = data.lines;
        const binauralUrl = data.binaural_url;
        const audioElement = document.getElementById('binaural-audio');
        audioElement.src = binauralUrl;

        let index = 0;
        function displayLine() {
            if (index >= lines.length) {
                index = 0; // Loop or end the session
            }
            const line = lines[index];
            const textOverlay = document.getElementById('text-overlay');
            textOverlay.textContent = line.text;

            // Optionally play line-specific audio
            if (line.audio_url) {
                const lineAudio = new Audio(line.audio_url);
                lineAudio.play();
            }

            index++;
            setTimeout(displayLine, line.display_duration * 1000);
        }

        displayLine();
    })
    .catch(error => {
        console.error('Error fetching session data:', error);
    });
});
