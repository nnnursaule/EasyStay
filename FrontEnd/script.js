
const slides = document.querySelectorAll('.slide');
const paginations = document.querySelectorAll('.pagination span');
let currentIndex = 0;
const totalSlides = slides.length;

function goToSlide(index) {
  slides.forEach((slide, i) => {
    slide.classList.toggle('current-slide', i === index);
  });

  paginations.forEach((dot, i) => {
    dot.classList.toggle('active', i === index);
  });
}

function nextSlide() {
  currentIndex = (currentIndex + 1) % totalSlides;
  goToSlide(currentIndex);
}

setInterval(nextSlide, 3000);


paginations.forEach((dot, index) => {
  dot.addEventListener('click', () => {
    currentIndex = index;
    goToSlide(currentIndex);
  });
});

goToSlide(currentIndex);



document.querySelectorAll(".faq-header").forEach((item) => {
  item.addEventListener("click", function () {
      const faqItem = this.parentElement;
      faqItem.classList.toggle("active");
      this.querySelector(".faq-toggle").textContent = faqItem.classList.contains("active") ? "✖" : "+";
  });
});


const textarea = document.getElementById("message");
textarea.addEventListener("input", () => {
  textarea.style.height = "auto";
  textarea.style.height = textarea.scrollHeight + "px";
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