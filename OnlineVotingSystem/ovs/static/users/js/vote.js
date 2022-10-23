function giveVote() {
  const partyId = document.querySelector(
    'input[name="selectedParty"]:checked'
  ).value;

  console.log(partyId);
  const data = {
    selectedParty: partyId,
  };

  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/giveVote", true);
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhr.send(JSON.stringify(data));
  console.log("req sent...");

  xhr.onreadystatechange = function () {
    if (xhr.readyState == XMLHttpRequest.DONE) {
      const serverResponse = JSON.parse(xhr.response);
      alert(serverResponse.message);
    }
  };
}

window.addEventListener("DOMContentLoaded", () => {
  console.log("load hua");
});
