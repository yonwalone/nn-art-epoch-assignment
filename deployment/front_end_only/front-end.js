let model

function init(){
  //model =  tf.loadLayersModel('https://cors-anywhere.herokuapp.com/C:/SteffensOrdner/Programmieren/Studienarbeit/nn-art-epoch-assignment/deployment/front_end_only/tfjs_model/model.json');
  model =  tf.loadLayersModel('tfjs_model/model.json');
}

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

  // Convert image
  console.log(file)
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