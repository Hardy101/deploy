// Go back to the previous page
function goBack() {
  window.history.back();
}
// Smooth Scrolling function
function smoothScroll(target) {
  let element = document.querySelector(target);
  element.scrollIntoView({
    behavior: "smooth",
  });
}

let isOpen = false;
// Dropdown Toggle Function
if (document.getElementById("dropdown-toggle")) {
  const dropdownToggle = document.getElementById("dropdown-toggle");
  const dropdownMenu = document.getElementById("dropdown-menu");
  const caretIcon = dropdownToggle.querySelector(".caret_icon");

  dropdownToggle.addEventListener("click", function () {
    isOpen = !isOpen;
    dropdownMenu.classList.toggle("show", isOpen);
    dropdownMenu.classList.toggle("hide", !isOpen);
    caretIcon.classList.toggle("caret-rotate", isOpen);
  });
}

// Dropdown Hover Function
const science_button = document.querySelector(".science");
const science_div = document.querySelector(".science-div");
const social_science_button = document.querySelector(".social-science");
const social_science_div = document.querySelector(".social-science-div");
const arts_button = document.querySelector(".arts");
const arts_div = document.querySelector(".arts-div");
const detail_div = document.querySelectorAll(".detail-div");
const exams_button = document.querySelector(".exams");
const exams_div = document.querySelector(".exams-div");
const exams_practice_button = document.querySelector(".exams-p");
const exams_practice_div = document.querySelector(".exams-p-div");

if (document.querySelector(".science")) {
  function showDept(divToShow) {
    detail_div.forEach((div) => {
      div.classList.add("hidden");
    });
    divToShow.classList.remove("hidden");
  }
  social_science_button.addEventListener("mouseover", () => {
    showDept(social_science_div);
  });
  science_button.addEventListener("mouseover", () => {
    showDept(science_div);
  });
  arts_button.addEventListener("mouseover", () => {
    showDept(arts_div);
  });
  exams_button.addEventListener("mouseover", () => {
    showDept(exams_div);
  });
  exams_practice_button.addEventListener("mouseover", () => {
    showDept(exams_practice_div);
  });
}

// All Menu Function
if (document.getElementById("toggle_btn")) {
  const toggle_btn = document.querySelectorAll(".toggle_btn");
  const dropmenu = document.getElementById("all_menu");
  const close_btn = document.querySelector(".close_btn");

  toggle_btn.forEach((toggle_btn) => {
    toggle_btn.addEventListener("click", function () {
      dropmenu.classList.remove("hidden");
      dropmenu.classList.add("animate__fadeInDown");
      document.body.classList.add("overflow-hidden");
    });
  });

  close_btn.addEventListener("click", function () {
    dropmenu.classList.add("animate__fadeOutUp");
    setTimeout(() => {
      dropmenu.classList.add("hidden");
      dropmenu.classList.remove("animate__fadeInDown", "animate__fadeOutUp");
    }, 300);
    document.body.classList.remove("overflow-hidden");
  });
}

// Share Div
share_links = document.querySelector(".share-div");
share_btn = document.querySelector(".share");
let isShareDivVisible = false;
if (document.querySelector(".share-div")) {
  share_btn.addEventListener("click", () => {
    if (isShareDivVisible) {
      share_links.classList.add("animate__fadeOutDown");
      setTimeout(() => {
        share_links.classList.add("hidden");
        share_links.classList.remove("animate__fadeOutDown");
      }, 600);
    } else {
      share_links.classList.remove("hidden");
      share_links.classList.add("animate__fadeInUp");
    }

    isShareDivVisible = !isShareDivVisible;
  });
}

// Notification Tab Function
const toggleButtons = document.querySelectorAll(".noticeToggle");
const notificationDiv = document.getElementById("notificationDiv");
toggleButtons.forEach((toggleButton) => {
  toggleButton.addEventListener("click", function () {
    notificationDiv.classList.toggle("active");
    toggleOverlay();
  });
});

const sideDivButton = document.querySelector(".sideMore");
const closeSideDivButton = document.querySelector("#closesidemore");
const sideDiv = document.querySelector("#sidemore");

closeSideDivButton.addEventListener("click", () => {
  sideDiv.classList.remove("active");
  toggleOverlay();
});
sideDivButton.addEventListener("click", function () {
  sideDiv.classList.toggle("active");
  toggleOverlay();
});

// Overlay Feature
const overlay_div = document.querySelector(".overlay");
function toggleOverlay() {
  overlay_div.classList.toggle("hidden");
}
overlay_div.addEventListener("click", () => {
  notificationDiv.classList.remove("active");
  sideDiv.classList.remove("active");
  toggleOverlay();
});

// Search Bar
const searchinput = document.getElementById('navSearch')
searchinput.addEventListener('focus', function(){
    toggleOverlay()
})

const studyToolsToggle = document.getElementById('studyToolsToggle')
const studyToolsDropdown = document.getElementById('studyToolsDropdown')
const toolsToggle = document.getElementById('toolsToggle')
const toolsDropdown = document.getElementById('toolsDropdown')


studyToolsToggle.addEventListener('click', function() {
        studyToolsDropdown.classList.toggle('h-0');
        studyToolsDropdown.classList.toggle('h-auto');
        studyToolsDropdown.classList.toggle('bg-gray-100');
});
toolsToggle.addEventListener('click', function() {
        toolsDropdown.classList.toggle('h-0');
        toolsDropdown.classList.toggle('h-auto');
        toolsDropdown.classList.toggle('bg-gray-100');
});

const sidebarlinks = document.querySelectorAll('.sidebarlink')
sidebarlinks.forEach((link)=>{
    link.addEventListener('click', function(){
        link.classList.toggle('active')
    })
})