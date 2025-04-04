let currentInput = "";

function updateDisplay(){
    document.getElementById('display').value = currentInput;
}

function sendToServer(value){
    if(value === 'C'){
        currentInput = "";
        updateDisplay();
        return;
    }
    if(value === '⌫'){
        currentInput = currentInput.slice(0, -1);
        updateDisplay();
        return;
    }
    if(value === '='){
        fetch('/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ expression: currentInput })
        })
        .then(response => response.json())
        .then(data => {
            if(data.error){
                alert(`Error: ${data.error}`);
            }
            else{
                currentInput = data.result.toString();
                updateDisplay();
            }
        })
        .catch(() => {
            alert("Error with conecting to server");
        });
        return;
    }
    currentInput+=value;
    updateDisplay();
}