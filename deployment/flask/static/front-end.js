function check(event) {
  event.preventDefault();

  // Get a reference to the table element by its ID
  const tableElement = document.getElementById("resultTable");

  // Check if the element exists
  if (tableElement) {
    // If it exists, remove it from the DOM
    tableElement.remove();
  }

  const input = document.getElementById("imageFile");
  const file = input.files[0];
  if (file == null) {
      let output = document.getElementById("epochs");
      output.innerHTML = `First upload Image`;
      return
  }

  let form = new FormData()
  form.append('file', file)

  fetch("/predict", {
    method: 'POST',
    body: form
  })
  .then(response => response.json())
  .then(prediction => {
    document.getElementById("epochs").innerText = "";

    // Get a reference to the HTML table element
    const table = document.createElement('table');
    table.id = "resultTable"
    table.class = "my-table"
    table.style.textAlign = "center"

    // Create a table header row
    const headerRow = table.insertRow();
    const nameHeader = headerRow.insertCell();
    const ageHeader = headerRow.insertCell();
    nameHeader.textContent = 'Epoch';
    ageHeader.textContent = 'Probability';

    headerRow.style.backgroundColor = "#3498db";
    headerRow.style.color = "#f2f2f2";

    // Loop through the data array and create a table row for each element
    for (let i = 0; i < prediction.length; i++) {
      const row = table.insertRow();
      const nameCell = row.insertCell();
      const ageCell = row.insertCell();
      nameCell.textContent = prediction[i][0];
      ageCell.textContent = prediction[i][1];
    }

    // Add the table to the HTML document
    let container = document.getElementById("table-container")
    container.appendChild(table);
  })
  .catch(error => {
    console.error(error);
  });
}

function previewImage() {
  const input = document.getElementById("imageFile");
  const file = input.files[0];
  const reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = function(event) {
    const imagePreview = document.getElementById("image-preview");
    const image = new Image();
    image.src = event.target.result;
    image.onload = function() {
      imagePreview.style.display = "block";
      imagePreview.innerHTML = `<img id="imgView" src="${image.src}" alt="Uploaded Image" class="image"/>`;
    };
  };
}