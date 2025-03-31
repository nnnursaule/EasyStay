//main
document.querySelectorAll(".heart-icon").forEach(heart => {
    heart.addEventListener("click", function() {
        heart.classList.toggle('active');
    });
});

function menuProfile() {
    const profileMenu = document.querySelector(".menu");
    profileMenu.classList.toggle("active");
}

function viewCard(evt, cityName) {

    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("cards");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("link-2");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "grid";
    evt.currentTarget.className += " active";
}

document.getElementById("defaultLink").click();

function menuLanguage(){
    const lang_btn = document.getElementById("languageButton");
    lang_btn.classList.toggle("hidden");
    
}


document.getElementById("logo2-img").addEventListener("click", function() {
    window.location.href = "main.html";
  });

  

  var imgIndex = 1;
  imagesOfapartment(imgIndex);
  
  function plusImgs(n) {
    imagesOfapartment(imgIndex += n);
  }
  
  function imagesOfapartment(n) {
    var i;
    var img = document.getElementsByClassName("apartment-images");
    if (n > img.length) {imgIndex = 1}
    if (n < 1) {imgIndex = img.length}
    for (i = 0; i < img.length; i++) {
      img[i].style.display = "none";  
    }
    img[imgIndex-1].style.display = "block";  
  }