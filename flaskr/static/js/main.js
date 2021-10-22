var userInput = document.querySelector(".user-input");
var enterBtn = document.querySelector(".enter-btn");
var removeBtn = document.querySelector(".remove-btn");
var artistUl = document.querySelector(".artist-ul");
var submitBtn = document.querySelector(".submit-btn");

submitBtn.addEventListener("click", function () {
  let artistItems = artistUl.getElementsByTagName("li");
  let artists = [];
  let url = "/created";

  for (var i = 0; i < artistItems.length; ++i) {
    artists.push(artistItems[i].innerText);
  }

  var artists_obj = { artists: artists };
  // console.log(artists_obj);

  const content = {
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(artists_obj),
    method: "POST",
  };

  // const URL = "/success";
  // const xhr = new XMLHttpRequest();
  // xhr.open("POST", URL);
  // xhr.send(data);
  fetch(url, content)
    .then((data) => {
      return data.json();
    })
    .then((res) => {
      console.log(res);
    })
    .catch((error) => {
      console.log(error);
    });

  artistUl.innerHTML = "";
});

enterBtn.addEventListener("click", function () {
  let artistDiv = document.createElement("div");
  let deleteBtn = document.createElement("button");
  let artist = document.createElement("li");

  artistDiv.classList.add("noselect");
  deleteBtn.classList.add("remove-btn", "close");
  deleteBtn.innerHTML = "&times;";
  deleteBtn.setAttribute("onclick", "deleteArtist(this);");
  artist.innerText = userInput.value;

  artistDiv.appendChild(artist);
  artistDiv.appendChild(deleteBtn);
  artistUl.appendChild(artistDiv);

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
