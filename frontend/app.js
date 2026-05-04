const API_BASE = "";

function renderCards(data) {

    const total =
        data.reduce(
            (sum,item)=>sum + item.total_incidents,
            0
        );

    const mttr =
        data.reduce(
            (sum,item)=>
                sum + (item.avg_resolution * item.total_incidents),
            0
        ) / total;

    const p95 =
        Math.max(
            ...data.map(
                item => item.p95_resolution
            )
        );

    const compliance =
        data.reduce(
            (sum,item)=>
                sum + (item.sla_compliance * item.total_incidents),
            0
        ) / total;

    const critical =
        data.find(
            item => item.severity === 3
        )?.total_incidents || 0;

    const breach =
        100 - compliance;


    document.getElementById("total").innerText =
        total;

    document.getElementById("mttr").innerText =
        mttr.toFixed(2);

    document.getElementById("p95").innerText =
        p95.toFixed(2);

    document.getElementById("sla_compliance").innerText =
        compliance.toFixed(2);

    document.getElementById("critical").innerText =
        critical;

    document.getElementById("breach").innerText =
        breach.toFixed(2);
}

function renderResolutionChart(data) {
    new Chart(document.getElementById("resolutionChart"), {
        type: "bar",
        data: {
            labels: data.map(item => `Severity ${item.severity}`),
            datasets: [{
                label: "Avg Resolution (min)",
                data: data.map(item => item.avg_resolution)
            }]
        }
    });
}

function renderSlaChart(data) {
    new Chart(document.getElementById("slaChart"), {
        type: "bar",
        data: {
            labels: data.map(item => `Severity ${item.severity}`),
            datasets: [{
                label: "SLA Compliance (%)",
                data: data.map(item => item.sla_compliance)
            }]
        }
    });
}

function renderP95Chart(data) {
    new Chart(document.getElementById("p95Chart"), {
        type: "bar",
        data: {
            labels: data.map(item => `Severity ${item.severity}`),
            datasets: [{
                label: "P95 Resolution (min)",
                data: data.map(item => item.p95_resolution)
            }]
        }
    });
}

function downloadReport() {
    window.open(`${API_BASE}/report`, "_blank");
}

async function loadMetrics() {
    try {
        const response = await fetch(`/metrics`);

        console.log("Status:", response.status);

        if (!response.ok) {
            throw new Error("Erro na API");
        }

        const data = await response.json();
        console.log("Dados recebidos:", data);

        renderCards(data);
        renderDistributionChart(data);
        renderResolutionChart(data);
        renderSlaChart(data);
        renderP95Chart(data);

    } catch (error) {
        console.error("Erro ao carregar métricas:", error);
    }
}

async function loadTrendChart() {

    const response =
        await fetch(`/metrics/daily`);

    const data =
        await response.json();


    const incidentsByDay = {};
    const complianceByDay = {};
    const countsByDay = {};


    data.forEach(item => {

        if (!incidentsByDay[item.day]) {

            incidentsByDay[item.day] = 0;
            complianceByDay[item.day] = 0;
            countsByDay[item.day] = 0;
        }

        incidentsByDay[item.day] +=
            item.total_incidents;

        complianceByDay[item.day] +=
            item.sla_compliance;

        countsByDay[item.day] += 1;
    });


    const labels =
        Object.keys(incidentsByDay);

    const incidentValues =
        Object.values(incidentsByDay);

    const complianceValues =
        labels.map(
            day =>
                (
                    complianceByDay[day] /
                    countsByDay[day]
                ).toFixed(2)
        );


    new Chart(
        document.getElementById(
            "trendChart"
        ),
        {
            type: "line",

            data: {
                labels,

                datasets: [
                    {
                        label:
                          "Incidents per Day",

                        data:
                          incidentValues,

                        yAxisID: "y"
                    },

                    {
                        label:
                          "SLA Compliance %",

                        data:
                          complianceValues,

                        yAxisID: "y1"
                    }
                ]
            },

            options: {
                responsive: true,

                scales: {

                    y: {
                        type: "linear",
                        position: "left"
                    },

                    y1: {
                        type: "linear",
                        position: "right",
                        min:0,
                        max:100
                    }
                }
            }
        }
    );
}

function renderDistributionChart(data) {

    new Chart(
        document.getElementById("distributionChart"),
        {
            type: "doughnut",

            data: {
                labels: data.map(
                    item => `Severity ${item.severity}`
                ),

                datasets: [{
                    label: "Incident Distribution",
                    data: data.map(
                        item => item.total_incidents
                    )
                }]
            },

            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: "bottom"
                    }
                }
            }
        }
    );
}

loadMetrics();
loadTrendChart();


