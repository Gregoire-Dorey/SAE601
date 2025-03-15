document.addEventListener("DOMContentLoaded", function() {
    let ctx = document.getElementById('monitoringChart').getContext('2d');

    let chartData = {
        labels: [],
        datasets: [{
            label: "Paquets envoyés",
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
                x: { title: { display: true, text: "Temps" } },
                y: { title: { display: true, text: "Paquets" }, beginAtZero: true }
            }
        }
    });

    let socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('update_graph', function(data) {
        let currentTime = new Date().toLocaleTimeString();

        if (chartData.labels.length > 20) {
            chartData.labels.shift();
            chartData.datasets[0].data.shift();
        }

        chartData.labels.push(currentTime);
        chartData.datasets[0].data.push(data.packets);
        monitoringChart.update();
    });

    socket.emit('start_monitoring');
});
