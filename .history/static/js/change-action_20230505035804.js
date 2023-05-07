function submitUpload(url = "") {
  // your code start here
  var data = new FormData();
  data.append("files", file); // maybe it should be '{target}_cand'
  data.append("name", file.name);

  fetch(url, {
    method: "POST",
    body: data,
  }).then(function (response) {
    return response.json();
  });
}

function changeAction(radio) {
  let url = "";
  if (radio.value === "option1") {
    url = "/flickr8k";
  } else if (radio.value === "option2") {
    url = "/flickr30k";
  } else if (radio.value === "option3") {
    url = "/VitGpt2ImageCaption";
  }
  document.getElementById("submit-upload").action = url;
  submitUpload(url);
}