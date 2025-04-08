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
    window.location.href = "main.daycont_html";
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


document.addEventListener("DOMContentLoaded", function() {

    class Calendars{
        constructor (monthChoose, yearChoose, daycont) {
            this.monthChoose = document.getElementById(monthChoose);
            this.yearChoose = document.getElementById(yearChoose);
            this.daycont = document.getElementById(daycont);

            this.changeDropdowns = this.changeDropdowns.bind(this);

            this.monthChoose.addEventListener('change', this.changeDropdowns);
            this.yearChoose.addEventListener('change', this.changeDropdowns);
        }

        yearDropdown(){
            let yeardrop = this.yearChoose;
            const presentYear = new Date().getFullYear();
    
            for (let i = presentYear; i <= presentYear + 5; i++) {
                const opt = document.createElement("option");
                opt.value = i;
                opt.textContent = i;
                yeardrop.appendChild(opt);
            }
        }

        show(month, year){
            this.daycont.innerHTML = '';
            const month_fstday = new Date(year, month, 1).getDay();
            const month_last_date = new Date(year, month + 1, 0).getDate();
            const month_last_wday = new Date(year, month, month_last_date).getDay();
            const prev_last = new Date(year, month, 0).getDate();

            const changed_fstday = month_fstday === 0 ? 6 : month_fstday - 1;
            this.monthChoose.value = month;
            this.yearChoose.value = year;

            let daycont_html = '';
            for (let i = changed_fstday; i > 0; i--){
                daycont_html += `<div class ="date-inactive">${prev_last - i + 1}</div>`;
            }

            for(let i = 1; i<=month_last_date; i++){
                daycont_html += `<div class = "date">${i}</div>`; 
            }

            for(let i = month_last_wday; i <= 6; i++){
                daycont_html += `<div class ="date-inactive">${i - month_last_wday + 1}</div>`;
            }

            this.daycont.innerHTML = daycont_html;
                

        }
        
        changeDropdowns() {
            const changeMonth = parseInt(this.monthChoose.value);
            const changeYear = parseInt(this.yearChoose.value);
            this.show(changeMonth, changeYear);
        }
    }


    today = new Date();
    currentMonth = today.getMonth();
    currentYear = today.getFullYear();

    const cal1 = new Calendars('month-c1', 'year-c1', 'daycont1');
    cal1.yearDropdown();
    cal1.show(currentMonth, currentYear);


    const cal2 = new Calendars('month-c2', 'year-c2', 'daycont2');
    cal2.yearDropdown();
    cal2.show(currentMonth, currentYear);



});
