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
