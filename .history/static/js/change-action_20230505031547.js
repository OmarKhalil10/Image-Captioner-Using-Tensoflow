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

  function submitUpload(url) {
    var data = new FormData();
    data.append("files", file);
    data.append("name", file.name);
  
    fetch(url, {
      method: "POST",
      body: data,
    })
    .then(function(response){
      return response.json()
    })
  }