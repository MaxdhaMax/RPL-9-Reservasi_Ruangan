const date = new Date();
var bookedDate = [];

const setBooked = (booked) => {
  bookedDate = booked;
}


async function getBookData(date) {
  var datestr = date.replaceAll("/","-");
  try{
    const roomId = window.location.href.slice(-1)
    const res = await fetch(`http://localhost:5000/calendar/${roomId}/${datestr}`)
    const book_data = await res.json()
    return await book_data
  }catch(error){
    console.log(error)
  }
}

function createModal(date) {
  const datestr = date.replaceAll("/","-");
  const modal  = `<div class="modal fade" id="${'modal-' + datestr}" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content bg-dark text-white">
      <div class="modal-header">
        <h1 class="modal-title" id="exampleModalLabel">Booked</h1>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <table class="table table-dark">
        <thead>
        </thead>
        <tbody>
          <tr>
            <th scope="row"><h3>Date</h3></th>
            <td><h3 class="date"></h3></td>
          </tr>
          <tr>
            <th scope="row"><h3>Held By</h3></th>
            <td><h3 class="event"></h3></td>
          </tr>
          <tr>
            <th scope="row"><h3>Event Held By</h3></th>
            <td colspan="2"><h3 class="organization"></h3></td>
          </tr>
          <tr>
            <th scope="row"><h3>Booked By</h3></th>
            <td colspan="2"><h3 class="booked_by"></h3></td>
          </tr>
        </tbody>
      </table>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</div>`
    return modal
}

function renderCalendar() {
  date.setDate(1);

  const monthDays = document.querySelector(".days");
  const modalGenerator = document.querySelector(".modalgenerator");
  monthDays.innerHTML = ""
  modalGenerator.innerHTML = ""
  const lastDay = new Date(
    date.getFullYear(),
    date.getMonth() + 1,
    0
  ).getDate();

  const prevLastDay = new Date(
    date.getFullYear(),
    date.getMonth(),
    0
  ).getDate();

  const firstDayIndex = date.getDay();

  const lastDayIndex = new Date(
    date.getFullYear(),
    date.getMonth() + 1,
    0
  ).getDay();
  
  var nextDays = null;
  if(Math.floor(firstDayIndex + lastDay > 7*5)){
      nextDays = 7 - lastDayIndex - 1;
  } else { 
      nextDays = 14 - lastDayIndex - 1; 
  }

  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  document.querySelector(".date h1").innerHTML = months[date.getMonth()] + " " + date.getFullYear();

  document.querySelector(".date p").innerHTML = new Date().toDateString();

  for (let x = firstDayIndex; x > 0; x--) {
    monthDays.innerHTML += `<div class="prev-date">${prevLastDay - x + 1}</div>`;
  }

  for (let i = 1; i <= lastDay; i++) {
    currentDate = `${date.getFullYear()}/${('0'+ (date.getMonth() + 1) ).slice(-2)}/${('0' + i).slice(-2)}`
    const id = `booked-${currentDate.replaceAll("/","-")}`
    console.log(currentDate)
    if (
      i === new Date().getDate() &&
      date.getMonth() === new Date().getMonth()
    ) {
      monthDays.innerHTML += `<div class="today">${i}</div>`;
    } else if(bookedDate.includes(currentDate)) {
      monthDays.innerHTML += `<div class="booked" id="${id}" 
      data-toggle="modal" data-target="${"#modal-" + currentDate.replaceAll("/","-")}">
      ${i}</div>`;
      modalGenerator.innerHTML += createModal(currentDate);
    } 
    else {
      monthDays.innerHTML += `<div class="empty" id="${id}">${i}</div>`;
    }
  }

  for (let j = 1; j <= nextDays; j++) {
    monthDays.innerHTML += `<div class="next-date">${j}</div>`;  
  }

  document.querySelectorAll(`.booked`).forEach(date => {
    date.addEventListener("click", async () => {
      const cleanDate = date.id.slice(7);
      const editDate = document.querySelector(`#modal-${cleanDate} .modal-body .date`)
      const editEvent = document.querySelector(`#modal-${cleanDate} .modal-body .event`)
      const editOrganization = document.querySelector(`#modal-${cleanDate} .modal-body .organization`)
      const editBookedBy = document.querySelector(`#modal-${cleanDate} .modal-body .booked_by`)
      const bookData = await getBookData(cleanDate);
      console.log(bookData)
      editDate.innerHTML = `${bookData.date}`
      editEvent.innerHTML = `${bookData.event}`
      editOrganization.innerHTML = `${bookData.organization}`
      editBookedBy.innerHTML = `${bookData['booked_by.username']}`
    });
  })
};

document.querySelector(".prev").addEventListener("click", () => {
  date.setMonth(date.getMonth() - 1);
  renderCalendar();
});

document.querySelector(".next").addEventListener("click", () => {
  date.setMonth(date.getMonth() + 1);
  renderCalendar();
});


