var userInput = document.querySelector(".user-input");
let enterBtn = document.querySelector(".enter-btn");
let removeBtn = document.querySelector(".remove-btn");
var artistList = document.querySelector(".artist-ul");
let submitBtn = document.querySelector(".submit-btn");

submitBtn.addEventListener("click", function () {
  artistList.innerHTML = "";
});

enterBtn.addEventListener("click", function () {
  var artistDiv = document.createElement("div");
  var deleteBtn = document.createElement("button");
  var artist = document.createElement("li");
  artistDiv.classList.add("noselect");
  deleteBtn.classList.add("remove-btn", "close");
  deleteBtn.innerHTML = "&times;";
  deleteBtn.setAttribute("onclick", "deleteArtist(this);");

  artist.innerText = userInput.value;
  artist.setAttribute("onclick", "move(this);");

  artistDiv.appendChild(artist);
  artistDiv.appendChild(deleteBtn);
  artistList.appendChild(artistDiv);

  userInput.value = "";
});

userInput.addEventListener("keyup", function (event) {
  if (event.keyCode == 13) {
    enterBtn.click();
  }
});

function deleteArtist(artistDel) {
  var artist = artistDel.parentNode;
  var list = artist.parentNode;
  list.removeChild(artist);
}
