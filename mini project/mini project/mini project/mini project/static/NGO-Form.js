// Get user's current location
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

// Set latitude and longitude values in hidden fields
function showPosition(position) {
    document.getElementById('latitude').value = position.coords.latitude.toFixed(6);
    document.getElementById('longitude').value = position.coords.longitude.toFixed(6);
}

// Handle geolocation errors
function showError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            alert("User denied the request for Geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            alert("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            alert("An unknown error occurred.");
            break;
    }
}

// Call getLocation function on page load
window.onload = function() {
    getLocation();
};


document.getElementById('animalForm').onsubmit = function(event) {
    event.preventDefault();  // Prevent the form from submitting the default way
    var formData = new FormData(this);
    
    fetch("{% url 'SubmitNgoForm' %}", {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
        },
    })
    .then(response => response.json())
    .then(data => {
        const messageDiv = document.getElementById('form-message');
        messageDiv.innerHTML = `<p>${data.message}</p>`;
        messageDiv.classList.add('success');
        messageDiv.style.display = 'block';  // Show the message div
    })
    .catch(error => {
        const messageDiv = document.getElementById('form-message');
        messageDiv.innerHTML = `<p>Form submission failed.</p>`;
        messageDiv.classList.add('error');
        messageDiv.style.display = 'block';  // Show the message div
        console.error('Error:', error);
    });
};
