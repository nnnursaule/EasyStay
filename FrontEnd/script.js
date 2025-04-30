const images = ["img/main1.png", "img/main2.png", "img/main3.png"];
let currentIndex = 0;

function changeImage(index) {
    document.querySelector(".hero").style.backgroundImage = `url(${images[index - 1]})`;
    document.querySelectorAll(".pagination span").forEach((dot, i) => {
        dot.classList.toggle("active", i === index - 1);
    });
}

document.querySelectorAll(".heart-icon").forEach(heart => {
    heart.addEventListener("click", function() {
        heart.classList.toggle('active');
    });
});
document.querySelectorAll(".faq-header").forEach((item) => {
    item.addEventListener("click", function () {
        const faqItem = this.parentElement;
        faqItem.classList.toggle("active");
        this.querySelector(".faq-toggle").textContent = faqItem.classList.contains("active") ? "✖" : "+";
    });
});

document.getElementById("goToTop").addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: "smooth" });
});
// raiting
document.getElementById("feedbackForm").addEventListener("submit", function(e) {
    e.preventDefault();
    const name = document.getElementById("name").value;
    const phone = document.getElementById("phone").value;
    const message = document.getElementById("message").value;
    const rating = document.querySelector('input[name="rating"]:checked');

    if (!name || !phone || !message) {
      alert("Please fill out all the fields.");
      return;
    }

    if (!rating) {
      alert("Please select a rating.");
      return;
    }

    alert("Feedback sent successfully! Rating: " + rating.value);
  });
  
// login

document.getElementById("openModal").addEventListener("click", function() {
document.getElementById("loginModal").style.display = "flex";
});

document.querySelector(".close").addEventListener("click", function() {
document.getElementById("loginModal").style.display = "none";
});

function openTab(evt, tabName) {
    let tabcontent = document.getElementsByClassName("tabcontent");
    let tablinks = document.getElementsByClassName("tablinks");

    for (let i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    for (let i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
    }

    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.classList.add("active");
}
