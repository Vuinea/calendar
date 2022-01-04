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

