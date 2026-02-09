// JavaScript for dynamic city dropdowns and payout calculation

document.addEventListener('DOMContentLoaded', function() {
    // Get the game map from the template context
    const gameMap = document.querySelector('h1').textContent.split(' - ')[1].split(' ')[0];
    
    // Fetch cities from the API and populate dropdowns
    fetchCities(gameMap);
    
    // Handle form submission
    const form = document.getElementById('cityForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            calculatePayout(gameMap);
        });
    }
    
    // Add swap button functionality
    const swapButton = document.getElementById('swapButton');
    const originSelect = document.getElementById('origin');
    const destinationSelect = document.getElementById('destination');
    
    if (swapButton && originSelect && destinationSelect) {
    swapButton.addEventListener('click', function() {
        // Set origin to previous destination value
        const destValue = destinationSelect.value;
        if (destValue) {
            originSelect.value = destValue;
        } else {
            originSelect.value = "";
        }
        // Clear destination selection
        destinationSelect.value = "";
        document.getElementById('payout-result').classList.add('hidden');
    });
    }
    
    // Handle input changes for real-time updates
    if (originSelect) {
        originSelect.addEventListener('change', function() {
            updateCityInput(this, 'origin-text');
        });
    }
    
    if (destinationSelect) {
        destinationSelect.addEventListener('change', function() {
            updateCityInput(this, 'destination-text');
        });
    }
});

function fetchCities(gameMap) {
    // Fetch cities from the API endpoint
    fetch(`/api/cities/${gameMap}`)
        .then(response => response.json())
        .then(data => {
            populateDropdowns(data.cities);
        })
        .catch(error => {
            console.error('Error fetching cities:', error);
        });
}

function populateDropdowns(cities) {
    const originSelect = document.getElementById('origin');
    const destinationSelect = document.getElementById('destination');
    
    if (!originSelect || !destinationSelect) return;
    
    // Clear existing options
    originSelect.innerHTML = '<option value="">Select a city</option>';
    destinationSelect.innerHTML = '<option value="">Select a city</option>';
    
    // Add cities to dropdowns
    cities.forEach(city => {
        const option = document.createElement('option');
        option.value = city;
        option.textContent = city;
        
        originSelect.appendChild(option.cloneNode(true));
        destinationSelect.appendChild(option);
    });
}

function updateCityInput(selectElement, inputId) {
    const input = document.getElementById(inputId);
    if (input) {
        // If user selects from dropdown, clear the text input
        input.value = '';
    }
}

function calculatePayout(gameMap) {
    const originSelect = document.getElementById('origin');
    const destinationSelect = document.getElementById('destination');
    const originText = document.getElementById('origin-text');
    const destinationText = document.getElementById('destination-text');
    
    let origin = '';
    let destination = '';
    
    // Get values from dropdowns or text inputs
    if (originSelect && originSelect.value) {
        origin = originSelect.value;
    } else if (originText && originText.value) {
        origin = originText.value;
    }
    
    if (destinationSelect && destinationSelect.value) {
        destination = destinationSelect.value;
    } else if (destinationText && destinationText.value) {
        destination = destinationText.value;
    }
    
    // Validate inputs
    if (!origin || !destination) {
        alert('Please select or enter both origin and destination cities.');
        return;
    }
    
    // Fetch payout from API
    fetch(`/api/payout/${gameMap}/${origin}/${destination}`)
        .then(response => response.json())
        .then(data => {
            displayPayoutResult(data.payout, origin, destination);
        })
        .catch(error => {
            console.error('Error calculating payout:', error);
            displayPayoutResult('Error calculating payout');
        });
}

function displayPayoutResult(payout, origin, destination) {
    const resultDiv = document.getElementById('payout-result');
    const payoutText = document.getElementById('payout-text');
    const payoutRoute = document.getElementById('payout-route')
    
    if (resultDiv && payoutText) {
        payoutRoute.textContent = `From ${origin} to ${destination}`;
        payoutText.textContent = `Payout: ${payout}`;
        resultDiv.classList.remove('hidden');
        
        // Scroll to results
        resultDiv.scrollIntoView({ behavior: 'smooth' });
    }
}