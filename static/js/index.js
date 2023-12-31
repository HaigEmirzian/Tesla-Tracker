let lastValue = null;

function fetchPortfolioValue() {
    fetch('/get_portfolio_value')
    .then(response => response.json())
    .then(data => {
        document.getElementById('portfolio-value').innerText = data.portfolio_value;
    })
    .catch(error => console.error('Error:', error));
}

setInterval(fetchPortfolioValue, 100000);