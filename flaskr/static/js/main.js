var userInput = document.querySelector(".user-input");
let enterBtn = document.querySelector(".enter-btn");
let removeBtn = document.querySelector(".remove-btn");
var artistList = document.querySelector(".artist-ul");
let submitBtn = document.querySelector(".submit-btn");

submitBtn.addEventListener("click", function () {
  var songs = artistList.getElementsByTagName("li");
  const artists = [];
  for (var i = 0; i < songs.length; ++i) {
    artists.push(songs[i].innerText);
  }
  artistList.innerHTML = "";
  var js_data = JSON.stringify(artists);
  $.ajax({
    url: "/getTopSongs",
    type: "post",
    contentType: "application/json",
    dataType: "json",
    data: js_data,
  })
    .done(function (result) {
      console.log(result);
      $("#data").html(result);
    })
    .fail(function (jqXHR, textStatus, errorThrown) {
      console.log("fail: ", textStatus, errorThrown);
    });
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
