document.addEventListener('DOMContentLoaded', function() {
    let guestCount = 1; // Start with guest 1

    // Get the button and the container for adding guests
    const addGuestButton = document.getElementById('add-guest-button');
    const guestContainer = document.getElementById('guest-container');

    // Add event listener to the "Add More Guests" button
    addGuestButton.addEventListener('click', function() {
      guestCount++; // Increment guest count to keep inputs unique

      // Create a new row for additional guest
      const newGuestRow = document.createElement('div');
      newGuestRow.classList.add('row', 'mb-4'); // Add row and margin classes

      // Create HTML for the new set of guest fields
      const newGuestFields = `
        <div class="col-auto">
          <label for="guest_name_${guestCount}" class="col-form-label">Guest Full Name</label>
        </div>
        <div class="col-auto">
          <input type="text" id="guest_name_${guestCount}" class="form-control" />
        </div>
        <div class="col-auto guest-field d-flex align-items-center">
          <input class="form-check-input" type="checkbox" id="guest_is_adult_${guestCount}" />
          <label class="form-check-label ms-1" for="guest_is_adult_${guestCount}">Is Adult</label>
        </div>
      `;

      // Add the new fields into the new row
      newGuestRow.innerHTML = newGuestFields;

      // Insert the new row before the button, to ensure button remains at the end
      guestContainer.appendChild(newGuestRow);
    });
  });