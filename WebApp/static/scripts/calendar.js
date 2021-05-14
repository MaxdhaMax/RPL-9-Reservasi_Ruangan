const date = new Date();
var bookedDate = [];
var selectedDate = [];
var roomPrice = 0;

const setBooked = (booked) => {
  bookedDate = booked;
}

const setRoomPrice = (price) => {
  roomPrice = price;
}


async function getBookData(date) {
  var datestr = date.replaceAll("/", "-");
  try {
    const roomId = window.location.href.slice(window.location.href.lastIndexOf("/") + 1)
    console.log(roomId)
    const baseURL = window.location.origin
    const res = await fetch(baseURL + `/calendar/${roomId}/${datestr}`)
    const book_data = await res.json()
    return await book_data
  } catch (error) {
    console.log(error)
  }
}

function createSelectedDate() {
  selectedDate.sort()
  let selectedDateGenerator = document.querySelector(".ruangan-terpilih ul")
  let submitSelectedDate = document.querySelector("#submitSelectedDate")
  selectedDateGenerator.innerHTML = `<li class="list-group-item bg-dark text-light">Kosong</li>`;
  submitSelectedDate.value = ""
  if(selectedDate.length != 0){
    selectedDateGenerator.innerHTML = ""
  }
  selectedDate.forEach(sd => {
    console.log(sd)
    selectedDateGenerator.innerHTML += `<li class="list-group-item bg-dark text-light">${sd}</li>`;
    submitSelectedDate.value += `${sd} `
  }) 
}

function clearAllSelectedDate(){
  selectedDate = [];
  let selectedDateGenerator = document.querySelector(".ruangan-terpilih ul")
  selectedDateGenerator.innerHTML = `<li class="list-group-item bg-dark text-light">Kosong</li>`;
  renderCalendar()
}

function editModal(){
  if(selectedDate.length == 0 ){
    alert("Anda Belum Memilih Ruangan, Klik Tanggal Pada Kalender Untuk Check In");
  }
  const selectedDateModal = document.querySelector("#modal-tanggal ul")
  const priceModal = document.querySelector("#modal-biaya")
  let priceSum = 0
  selectedDateModal.innerHTML = ""
  priceModal.innerHTML = ""
  if(selectedDate.length == 0){
    selectedDateModal.innerHTML = `<li class="list-group-item bg-dark text-light">Kosong</li>`
  }
  selectedDate.forEach(sd => {
    selectedDateModal.innerHTML += `<li class="list-group-item bg-dark text-light">${sd}</li>`
    priceSum += roomPrice;
  })
  priceModal.innerHTML = `Rp ${priceSum}`;
}

function submitDate(){
  const form = document.querySelector("#selectedDateForm")
  if(selectedDate.length != 0){
    form.submit()
  }else{
    alert("Anda Belum Memilih Ruangan, Klik Tanggal Pada Kalender Untuk Check In")
  }
}
function createModal(date) {
  const datestr = date.replaceAll("/", "-");
  const modal = `<div class="modal fade" id="${'modal-' + datestr}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content bg-dark text-white">
      <div class="modal-header">
        <h2 class="modal-title text-danger" id="exampleModalLabel">Booked</h2>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <table class="table table-dark">
        <thead>
        </thead>
        <tbody>
          <tr>
            <th scope="row"><h5>Date</h5></th>
            <td><h5 class="date"></h5></td>
          </tr>
          <tr>
            <th scope="row"><h5>Event Name</h5></th>
            <td><h5 class="event"></h5></td>
          </tr>
          <tr>
            <th scope="row"><h5>Event Held By</h5></th>
            <td colspan="2"><h5 class="organization"></h5></td>
          </tr>
          <tr>
            <th scope="row" class="text-danger"><h4>Booked By</h4></th>
          </tr>
          <tr>
            <th scope="row"><h5>Full Name</h5></th>
            <td colspan="2"><h5 class="booked_by_name"></h5></td>
          </tr>
          <tr>
            <th scope="row"><h5>Username</h5></th>
            <td colspan="2"><h5 class="booked_by_username"></h5></td>
          </tr>
        </tbody>
        </table>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary bg-danger" data-bs-dismiss="modal">Close</button>
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
  if (Math.floor(firstDayIndex + lastDay > 7 * 5)) {
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

  document.querySelector(".date h2").innerHTML = months[date.getMonth()] + " " + date.getFullYear();


  for (let x = firstDayIndex; x > 0; x--) {
    monthDays.innerHTML += `<div class="prev-date">${prevLastDay - x + 1}</div>`;
  }

  for (let i = 1; i <= lastDay; i++) {
    currentDate = `${date.getFullYear()}/${('0' + (date.getMonth() + 1)).slice(-2)}/${('0' + i).slice(-2)}`
    const id = `booked-${currentDate.replaceAll("/", "-")}`
    const modalTarget = `${'#modal-' + currentDate.replaceAll("/", "-")}`

    if (bookedDate.includes(currentDate)) {
      monthDays.innerHTML += `<div class="booked" id="${id}" 
      data-bs-toggle="modal" data-bs-target="${modalTarget}">${i}</div>`;
      modalGenerator.innerHTML += createModal(currentDate);
    }
    else if(selectedDate.includes(currentDate)) {
      monthDays.innerHTML += `<div class="empty selected" id="${id}">${i}</div>`;
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
      const editBookedByName = document.querySelector(`#modal-${cleanDate} .modal-body .booked_by_name`)
      const editBookedByUsername = document.querySelector(`#modal-${cleanDate} .modal-body .booked_by_username`)
      try {
        const bookData = await getBookData(cleanDate);
        editDate.innerHTML = `${bookData.date}`
        editEvent.innerHTML = `${bookData.event}`
        editOrganization.innerHTML = `${bookData.organization}`
        editBookedByName.innerHTML = `${bookData.name}`
        editBookedByUsername.innerHTML = `${bookData['booked_by.username']}`
      } catch (error) {
        editDate.innerHTML = `ERROR 505`
        editEvent.innerHTML = `ERROR 505`
        editOrganization.innerHTML = `ERROR 505`
        editBookedByName.innerHTML = `ERROR 505`
        editBookedByUsername.innerHTML = `ERROR 505`
        console.log(error)
      }
    });
  })

  

  document.querySelectorAll('.empty').forEach(date => {
    function removeSelected(){
      console.log("remove selected")
      date.classList.remove("selected")
      const cleanDate = date.id.slice(7).replaceAll("-","/");
      selectedDate = selectedDate.filter(dateItems => dateItems!==cleanDate)
      createSelectedDate()
      date.addEventListener("click",addSelected)
      date.removeEventListener("click", removeSelected)
      console.log(selectedDate)
    }
    function addSelected(){
      console.log("selected")
      date.classList.add("selected");
      const cleanDate = date.id.slice(7).replaceAll("-","/");
      selectedDate.push(cleanDate);
      createSelectedDate()
      date.addEventListener("click",removeSelected)
      date.removeEventListener("click", addSelected)
      console.log(selectedDate)
    }
    if(date.classList.contains("selected")){
      date.addEventListener("click", removeSelected);
    }
    else{
      date.addEventListener("click", addSelected);
    }
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

