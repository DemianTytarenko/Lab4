document.getElementById('inputForm').addEventListener('submit', function(event) {
    event.preventDefault(); 
    var functionInput = document.getElementById('function').value;
    var startInput = document.getElementById('start').value;
    var endInput = document.getElementById('end').value;
    var url = '/api?function=' + encodeURIComponent(functionInput) +
              '&start=' + encodeURIComponent(startInput) +
              '&end=' + encodeURIComponent(endInput);

    getResult(url);
});

function getResult(url) {
    var resultElement = document.getElementById('result');
    resultElement.textContent = 'Loading...';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.onload = function() {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.hasOwnProperty('result')) {
                resultElement.textContent = 'Result: ' + response.result;
            } else if (response.hasOwnProperty('error')) {
                resultElement.textContent = 'Error: ' + response.error;
            }
        } else {
            resultElement.textContent = 'Error: ' + xhr.statusText;
        }
    };
    xhr.onerror = function() {
        resultElement.textContent = 'Error: Network Error';
    };
    xhr.send();
}