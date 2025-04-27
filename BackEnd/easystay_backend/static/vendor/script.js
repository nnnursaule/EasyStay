
let currentIndex = 0;

function changeImage(index) {
    document.querySelector(".hero").style.backgroundImage = `url(${images[index - 1]})`;
    document.querySelectorAll(".pagination span").forEach((dot, i) => {
        dot.classList.toggle("active", i === index - 1);
    });
}

document.getElementById("languageButton").addEventListener("click", function () {
    document.getElementById("languageDropdown").classList.toggle("hidden");
});

document.querySelectorAll("#languageDropdown a").forEach(item => {
    item.addEventListener("click", function (e) {
        e.preventDefault();
        window.location.href = this.getAttribute("href");
    });
});

document.addEventListener("click", function (event) {
    if (!document.querySelector(".language-container").contains(event.target)) {
        document.getElementById("languageDropdown").classList.add("hidden");
    }
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
