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
