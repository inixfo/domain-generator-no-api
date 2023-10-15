// Function to show the loading animation and hide the form
function showLoadingAnimation() {
    document.getElementById('formContainer').style.display = 'none';
    document.getElementById('loadingContainer').style.display = 'block';
}

// Function to hide the loading animation and show the suggestions
function showSuggestions(suggestions) {
    document.getElementById('loadingContainer').style.display = 'none';
    document.getElementById('suggestionsContainer').style.display = 'block';
    var suggestionsList = document.getElementById('suggestionsList');
    suggestionsList.innerHTML = '';
    suggestions.forEach(function(suggestion) {
        var li = document.createElement('li');
        li.appendChild(document.createTextNode(suggestion));
        suggestionsList.appendChild(li);
    });
}

// Function to handle form submission
function handleSubmit(event) {
    event.preventDefault();
    var domainType = document.getElementById('domain_type').value;
    var prompt = document.getElementById('prompt').value;
    var domainExtension = document.getElementById('domain_extension').value;
    var requestData = {
        domain_type: domainType,
        prompt: prompt,
        domain_extension: domainExtension
    };

    showLoadingAnimation();

    axios.post('/suggest', requestData)
        .then(function(response) {
            var suggestions = response.data.suggestions;
            showSuggestions(suggestions);
        })
        .catch(function(error) {
            console.error(error);
        });
}

// Attach event listener to form submit
document.getElementById('generateBtn').addEventListener('click', handleSubmit);
