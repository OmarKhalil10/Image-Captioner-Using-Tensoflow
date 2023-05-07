function changeAction(radio) {
    if (radio.value === "option1") {
      document.getElementById("submit-upload").action = "/flickr8k";
    } else if (radio.value === "option2") {
      document.getElementById("submit-upload").action = "/flickr30k";
    } else if (radio.value === "option3") {
      document.getElementById("submit-upload").action = "/VitGpt2ImageCaption";
    }
  }