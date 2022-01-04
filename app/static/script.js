const toggleDivVisibility = (id) => {
  const ele = document.getElementById(id);
  if (ele.style.display === "block") {
    ele.style.display = "none";
  } else {
    ele.style.display = "block";
  }
}

// this is for the day_view when you click the title then the body will expdnd

const displayExtraInfo = (item) => {
  const itemNum = item.id.slice(-1)
  const currentStyle = document.getElementById(`extra-info-${itemNum}`).style.display;
  if (currentStyle === "block") {
    document.getElementById(`extra-info-${itemNum}`).style.display = "none";
  } else {
    document.getElementById(`extra-info-${itemNum}`).style.display = "block";
  }
}

// the modal on the month view


const modal = document.getElementById("add-item-modal");
const closeBtn = document.getElementsByClassName("close")[0];
const dateInput = document.getElementById("modal-add-due");

closeBtn.onclick = () => {
  modal.style.display = "none";
}

window.onclick = (event) => {
  if (event.target === modal) {
    modal.style.display = "none";
  }
}

function changeValue(date) {
  const splitDate = date.split("-");
  const day = splitDate[2];
  const month = splitDate[1]

  if (day.length === 1) {
    splitDate[2] = "0" + day;
  }

  if (month.length === 1) {
    splitDate[1] = "0" + month;
  }

  date = splitDate.join("-")
  dateInput.value = date;
  modal.style.display = "block"

}
