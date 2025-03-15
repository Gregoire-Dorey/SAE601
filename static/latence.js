document.addEventListener("DOMContentLoaded", function() {
    const testForm = document.getElementById('latency-form');
    const resultDiv = document.getElementById('result');

    testForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const ip = document.getElementById('ip_switch').value;
        const name = document.getElementById('device_name').value || 'Switch';
        const numTrames = parseInt(document.getElementById('num_trames').value) || 10;

        // Afficher message de chargement
        resultDiv.innerHTML = '<p>Test en cours...</p>';

        fetch('/api/test_latence', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ip: ip,
                name: name,
                num_trames: numTrames
            })
        })
        .then(response => response.json())
        .then(data => {
            resultDiv.innerHTML = `
                <div class="result-card">
                    <h3>Résultats</h3>
                    <p>Appareil: ${data.name} (${data.ip})</p>
                    <p>Latence moyenne: ${data.latence} ms</p>
                    <p>Latence minimale: ${data.min} ms</p>
                    <p>Latence maximale: ${data.max} ms</p>
                </div>
            `;
        })
        .catch(error => {
            resultDiv.innerHTML = `<p class="error">Erreur: ${error.message}</p>`;
        });
    });
});