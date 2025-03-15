document.addEventListener("DOMContentLoaded", function() {
    let ctx = document.getElementById('monitoringChart').getContext('2d');

    let chartData = {
        labels: [],
        datasets: [{
            label: "Latence (ms)",
            borderColor: "rgba(75,192,192,1)",
            backgroundColor: "rgba(75,192,192,0.2)",
            data: [],
            fill: true,
        }]
    };

    let monitoringChart = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { title: { display: true, text: "Mesures" } },
                y: {
                    title: { display: true, text: "Latence (ms)" },
                    beginAtZero: true,
                    suggestedMax: 50
                }
            }
        }
    });

    // Connexion SocketIO
    let socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // Récupérer les données initiales
    fetch('/api/latency_history')
        .then(response => response.json())
        .then(data => {
            // Mettre à jour le graphique avec les données historiques
            chartData.labels = data.devices;
            chartData.datasets[0].data = data.latencies;
            monitoringChart.update();
        });

    // Écouter les nouvelles données de latence
    socket.on('new_latency_data', function(data) {
        // Ajouter la nouvelle donnée à notre graphique
        if (chartData.labels.length > 20) {
            chartData.labels.shift();
            chartData.datasets[0].data.shift();
        }

        chartData.labels.push(`${data.name} (${data.ip})`);
        chartData.datasets[0].data.push(data.latence);
        monitoringChart.update();
    });

    // Demander les données de monitoring
    socket.emit('request_monitoring_data');
});