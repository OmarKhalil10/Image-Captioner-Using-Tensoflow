let url = "/VitGpt2ImageCaption"

function changeAction(radio) {
    if (radio.value === "option1") {
      url = "/flickr8k";
    } else if (radio.value === "option2") {
      url = "/flickr30k";
    } else if (radio.value === "option3") {
      url = "/VitGpt2ImageCaption";
    }
    document.getElementById("submit-upload").action = url;
  }

  function submitUpload() {
    var fileInput = document.getElementById('fileUpload');
    var file = fileInput.files[0];
    
    var data = new FormData();
    data.append("image", file);
  
    fetch(url, {
      method: "POST",
      body: data,
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Error uploading file: ' + response.statusText);
      }
      return response.json();
    })
    .then(data => {
      // Handle response data
      console.log(data);
    })
    .catch(error => {
      console.error(error);
    });
  }