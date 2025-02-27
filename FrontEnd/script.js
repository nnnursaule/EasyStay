const images = ["image1.jpg", "image2.jpg", "image3.jpg"];
let currentIndex = 0;

function changeImage(index) {
    document.querySelector(".hero").style.backgroundImage = `url(${images[index - 1]})`;
    document.querySelectorAll(".pagination span").forEach((dot, i) => {
        dot.classList.toggle("active", i === index - 1);
    });
}

document.querySelectorAll(".faq-header").forEach((item) => {
    item.addEventListener("click", function () {
        const faqItem = this.parentElement;
        faqItem.classList.toggle("active");

        const button = this.querySelector(".faq-toggle");
        button.textContent = faqItem.classList.contains("active") ? "✖" : "+";
    });
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
