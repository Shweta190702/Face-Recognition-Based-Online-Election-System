// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ["ZYX", "YXZ", "PQR", "XYA", "RMS", "Others"],
    datasets: [{
      data: [3, 9, 2, 1, 0, 0],
      backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#4e73ff', '#1cc8aa', '#36b99c'],
      hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf', '#2e59dd', '#17a677', '#2c9faa'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});
