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

// document.getElementById("defaultLink").click();

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


//   function toggleDropdown(dropdown) {
//     document.getElementById(dropdown).classList.toggle("active");
//   }

  

  document.addEventListener("DOMContentLoaded", function() {

    class Calendars{
        constructor (monthChoose, yearChoose, daycont) {
            this.monthChoose = document.getElementById(monthChoose);
            this.yearChoose = document.getElementById(yearChoose);
            this.daycont = document.getElementById(daycont);


            this.changeDropdowns = this.changeDropdowns.bind(this);
            this.monthChoose.addEventListener('change', this.changeDropdowns, this.ne);
            this.yearChoose.addEventListener('change', this.changeDropdowns);

            this.date = new Date();
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

            for (let i = changed_fstday; i > 0; i--){
                const date = new Date(year, month - 1, prev_last - i + 1);
                const daycontDiv = document.createElement('div');
                daycontDiv.className = 'date inactive';
                daycontDiv.textContent = prev_last - i + 1;
                daycontDiv.dataset.date = date;
                this.daycont.appendChild(daycontDiv);

                
            }
            const today = new Date();
            for(let i = 1; i<=month_last_date; i++){
                const date = new Date(year, month, i);
                const daycontDiv = document.createElement('div');
                daycontDiv.className = 'date';
                daycontDiv.textContent = i;
                daycontDiv.dataset.date = date;
                if((date.getFullYear() == today.getFullYear()) && (date.getMonth() == today.getMonth()) && (date.getDate() == today.getDate())){
                    daycontDiv.classList.add('today');
                }

                this.daycont.appendChild(daycontDiv);
            }
            

            for(let i = month_last_wday; i <= 6; i++){
                const date = new Date(year, month + 1, i - month_last_wday + 1);
                const daycontDiv = document.createElement('div');
                daycontDiv.className = 'date inactive';
                daycontDiv.textContent = i - month_last_wday + 1;
                daycontDiv.dataset.date = date;
                this.daycont.appendChild(daycontDiv);
            }
        }
        
        changeDropdowns() {
            const changeMonth = parseInt(this.monthChoose.value);
            const changeYear = parseInt(this.yearChoose.value);
            this.show(changeMonth, changeYear);
        }

        getThisMonth() {
            return parseInt(this.monthChoose.value);
        }

        getThisYear() {
            return parseInt(this.yearChoose.value);
        }

        prev(){
            let year = parseInt(this.yearChoose.value);
            let prevmonth = parseInt(this.monthChoose.value);
            this.date = new Date(year, prevmonth);
            if(this.date > new Date(2025, 0) && this.date < new Date(2030, 11)){
                if(prevmonth>=0 && prevmonth <= 11){
                    prevmonth--;
                    year = year;
                }
                if(prevmonth < 0){
                    year--;
                    prevmonth = 11;
                }
                this.show(prevmonth, year);

            }
    
        }
        next(){
            let nextmonth = parseInt(this.monthChoose.value);
            let yearnext = parseInt(this.yearChoose.value);
            this.date = new Date(yearnext, nextmonth);

            if(this.date >= new Date(2025, 0) && this.date < new Date(2030, 11)){
                if(nextmonth>=0 && nextmonth <= 11){
                    nextmonth++;
                    yearnext = yearnext;
                }
                if(nextmonth > 11){
                    yearnext++;
                    nextmonth = 0;
                }
                this.show(nextmonth, yearnext);

            }
        }

        
    }
    const takenDates = [
        '01/04/2025', '02/04/2025','03/04/2025', '04/04/2025', '05/04/2025'
      ];
    let first_date = null;
    let snd_date = null; 
    

    function showUnavailable() {
        document.querySelectorAll('.date').forEach(date => {
            const dateEl = new Date(date.dataset.date);
            if(takenDates.includes(dateEl.toLocaleDateString("en-GB"))){
                date.classList.add('unavailable');
            }
    
        });
    }

    function select() {
        document.querySelectorAll('.date:not(.inactive):not(.unavailable)').forEach(date => {
            date.addEventListener('click', () => selectDate(date));
        });
        highlightSelectedDates();
    }

    function selectDate(day){        
        const selectedDate = new Date(day.dataset.date);
        const date_output = document.querySelector('p.date-text')
        if (!first_date || (first_date && snd_date)) {
            first_date = selectedDate;
            snd_date = null;
        } else if (selectedDate < first_date) {
            first_date = selectedDate;
        } else {
            snd_date = selectedDate;
        }
        const output = {
            day: "numeric",  
            month: "long",     
            year: "numeric"
          };
        if(first_date && snd_date){
            const start_output = first_date.toLocaleDateString("en-GB", output);
            const end_output = snd_date.toLocaleDateString("en-GB", output);
            date_output.innerHTML = `${start_output} - ${end_output}`;
        }
        
        highlightSelectedDates();
    }

    function highlightSelectedDates() {
        document.querySelectorAll('.date').forEach(el => {
            el.classList.remove('range-start', 'in-range', 'range-end');
            if(!el.classList.contains('inactive')){
                const date = new Date(el.dataset.date);
                if (first_date && date.getTime() === first_date.getTime()) {
                    el.classList.add('range-start');
                }
                if (snd_date && date.getTime() === snd_date.getTime()) {
                    el.classList.add('range-end');
                }
                if (first_date && snd_date && date > first_date && date < snd_date) {
                    el.classList.add('in-range');
                    console.log(el.className);
                }
            }
            else{
                const date = new Date(el.dataset.date);
                if (first_date && snd_date && date > first_date && date < snd_date) {
                    el.classList.add('in-range');
                    console.log(el.className);
                }
            }

        });

    }
    

    today = new Date();
    currentMonth = today.getMonth();
    currentYear = today.getFullYear();

    const cal1 = new Calendars('month-c1', 'year-c1', 'daycont1');
    cal1.yearDropdown();
    cal1.show(currentMonth, currentYear);

    const cal2 = new Calendars('month-c2', 'year-c2', 'daycont2');
    cal2.yearDropdown();
    cal2.show(currentMonth + 1, currentYear);

    
    document.getElementById('nextmonth').addEventListener('click', ()=>{
            cal2.next();
            cal1.next();
            select();
            showUnavailable();
    });
    cal1.monthChoose.addEventListener('change', () =>{
        const firstMonth = cal1.getThisMonth();
        const firstYear = cal1.getThisYear();

        cal2.show(firstMonth + 1, firstYear);
        select();
        showUnavailable();
    });

    cal1.yearChoose.addEventListener('change', () =>{
        const firstMonth = cal1.getThisMonth();
        const firstYear = cal1.getThisYear();

        cal2.show(firstMonth + 1, firstYear);
        select();
        showUnavailable();
    });

    cal2.monthChoose.addEventListener('change', () =>{
        const firstMonth = cal2.getThisMonth();
        const firstYear = cal2.getThisYear();

        cal1.show(firstMonth - 1, firstYear);
        select();
        showUnavailable();
    });

    cal2.yearChoose.addEventListener('change', () =>{
        const firstMonth = cal2.getThisMonth();
        const firstYear = cal2.getThisYear();

        cal1.show(firstMonth - 1, firstYear);
        select();
        showUnavailable();
    });
    document.getElementById('prevmonth').addEventListener('click', ()=>{
        cal1.prev();
        cal2.prev();
        select();
        showUnavailable();
    });
    
    select();
    showUnavailable();


});


function initMap(){


    const position ={lat: 43.2178314, lng: 76.8700653}
    const mapDetail = {
        center: position,
        zoom: 12,
        disableDefaultUI: true
    }
    const map = new google.maps.Map(document.getElementById('map'), mapDetail);

    const map_marker = {
        url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg" id="map-marker">
                <g>
                    <rect width="100" height="60"  rx="30" ry="30" fill="#FF5A30" />
                    <text x="20" y="38" font-family="Verdana" font-size="25px" fill="#022442" font-weight="550">350k</text>
                    <polygon points="10,45 34,45 22,93" style="fill:#FF5A30"/>
                </g>
            </svg>`),
        scaledSize: new google.maps.Size(90, 90),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(22, 93),
      };

      

      new google.maps.Marker({
        position: { lat: 43.2413323, lng: 76.9541664},
        map: map,
        icon: map_marker,
      });

      

}

window.onload = initMap;

