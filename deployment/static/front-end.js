function check(event) {
  event.preventDefault();

  const input = document.getElementById("imageFile");
  const file = input.files[0];
  if (file == null) {
      let output = document.getElementById("epochs");
      output.innerHTML = `First upload Image`;
      return
  }
  
  fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify([file])
  })
  .then(response => response.json())
  .then(prediction => {
    console.log("Response:")
    console.log(prediction)
    document.getElementById("epochs").innerText = `Prediction: ${prediction}`;
  })
  .catch(error => {
    console.error(error);
  });

  const output = document.getElementById("epochs");
  output.innerHTML = `Loading...`;
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
      imagePreview.innerHTML = `<img src="${image.src}" alt="Uploaded Image" class="image"/>`;
    };
  };
}