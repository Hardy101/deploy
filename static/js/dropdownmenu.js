let dropdownToggle = document.getElementById("dropdown-toggle");
let dropdownMenu = document.getElementById("dropdown-menu");
let isOpen = false;
let caretIcon = dropdownToggle.querySelector(".caret_icon");

dropdownToggle.addEventListener("click", function () {
  if (!isOpen) {
    dropdownMenu.classList.add("show");
    dropdownMenu.classList.remove("hide");
    caretIcon.classList.add("caret-rotate");
    isOpen = true;
  } else {
    dropdownMenu.classList.remove("show");
    dropdownMenu.classList.add("hide");
    caretIcon.classList.remove("caret-rotate");
    isOpen = false;
  }
});
