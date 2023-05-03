function changeAction(radio) {
    if (radio.value === "option1") {
      document.getElementById("myForm").action = "/flickr8k";
    } else if (radio.value === "option2") {
      document.getElementById("myForm").action = "/flickr30k";
    } else if (radio.value === "option3") {
      document.getElementById("myForm").action = "/VitGpt2ImageCaption";
    }
  }