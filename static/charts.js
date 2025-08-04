/*
document.addEventListener("DOMContentLoaded", function () {
  const { sentimentCounts, latestLabel, latestScore } = sentimentData;

  // Bar Chart
  const barCtx = document.getElementById("barChart").getContext("2d");
  new Chart(barCtx, {
    type: "bar",
    data: {
      labels: sentimentCounts.map(item => item._id),
      datasets: [{
        label: "Sentiment Count",
        data: sentimentCounts.map(item => item.count),
        backgroundColor: ["#4caf50", "#ffca28", "#f44336"]
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: { display: true, text: "Sentiment Distribution" }
      }
    }
  });

  // Pie Chart (Confidence of latest)
  const pieCtx = document.getElementById("pieChart").getContext("2d");
  new Chart(pieCtx, {
    type: "pie",
    data: {
      labels: ["Confidence", "Remaining"],
      datasets: [{
        data: [latestScore, 1 - latestScore],
        backgroundColor: ["#4caf50", "#e0e0e0"]
      }]
    },
    options: {
      plugins: {
        title: {
          display: true,
          text: `Latest Sentiment: ${latestLabel.toUpperCase()}`
        }
      }
    }
  });
});
*/

document.addEventListener("DOMContentLoaded", () => {
  const { latestScores, latestLabel, latestScore } = sentimentData;

  const barCtx = document.getElementById("barChart").getContext("2d");
  new Chart(barCtx, {
    type: "bar",
    data: {
      labels: sentimentData.latestScores.map(s => s.label),
      datasets: [{
        label: "Latest Sentiment Scores",
        data: sentimentData.latestScores.map(s => s.score),
        backgroundColor: ["#4caf50", "#f44336", "#ffc107"]
      }]
    },
    options: {
      scales: {
        y: { beginAtZero: true, max: 1 }
      },
      plugins: {
        title: {
          display: true,
          text: "Breakdown of Latest Sentiment"
        }
      }
    }
  });

  const pieCtx = document.getElementById("pieChart").getContext("2d");
  new Chart(pieCtx, {
    type: "pie",
    data: {
      labels: ["Confidence", "Remaining"],
      datasets: [{
        data: [latestScore, 1 - latestScore],
        backgroundColor: ["#4caf50", "#e0e0e0"]
      }]
    },
    options: {
      plugins: {
        title: {
          display: true,
          text: `Top Sentiment: ${latestLabel.toUpperCase()}`
        }
      }
    }
  });
});




/*
const labels = Object.keys(sentimentCounts);
const data = Object.values(sentimentCounts);

new Chart(document.getElementById('barChart'), {
  type: 'bar',
  data: {
    labels: labels,
    datasets: [{
      label: 'Sentiment Distribution',
      data: data,
      backgroundColor: ['#27ae60', '#e74c3c', '#f1c40f']
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: false }
    }
  }
});

new Chart(document.getElementById('pieChart'), {
  type: 'pie',
  data: {
    labels: labels,
    datasets: [{
      label: 'Sentiment',
      data: data,
      backgroundColor: ['#27ae60', '#e74c3c', '#f1c40f']
    }]
  },
  options: {
    responsive: true
  }
});
*/