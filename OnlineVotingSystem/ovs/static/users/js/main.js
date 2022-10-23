window.addEventListener("DOMContentLoaded", () => {
  document
    .getElementById("signInButton")
    .addEventListener("click", displayCameraMessage);

  function displayCameraMessage() {
    document.getElementById("cameraMessage").innerText =
      "Face Recognition in Progress, Please Look at the screen";
  }
});
