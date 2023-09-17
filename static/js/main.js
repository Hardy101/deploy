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
const science_button = document.querySelector('.science')
const science_div = document.querySelector('.science-div')
const social_science_button = document.querySelector('.social-science')
const social_science_div = document.querySelector('.social-science-div')
const arts_button = document.querySelector('.arts')
const arts_div = document.querySelector('.arts-div')
const detail_div = document.querySelectorAll('.detail-div')
const exams_button = document.querySelector('.exams')
const exams_div = document.querySelector('.exams-div')
const exams_practice_button = document.querySelector('.exams-p')
const exams_practice_div = document.querySelector('.exams-p-div')

if (document.querySelector('.science')){
function showDept(divToShow){
    detail_div.forEach((div)=>{
        div.classList.add('hidden')
    })
    divToShow.classList.remove('hidden')
}
social_science_button.addEventListener('mouseover', ()=>{
    showDept(social_science_div)
})
science_button.addEventListener('mouseover', ()=>{
    showDept(science_div)
})
arts_button.addEventListener('mouseover', ()=>{
    showDept(arts_div)
})
exams_button.addEventListener('mouseover', ()=>{
    showDept(exams_div)
})
exams_practice_button.addEventListener('mouseover', ()=>{
    showDept(exams_practice_div)
})
}

// All Menu Function
if (document.getElementById("toggle_btn")) {
  const toggle_btn = document.querySelectorAll(".toggle_btn");
  const dropmenu = document.getElementById("all_menu");
  const close_btn = document.querySelector('.close_btn');

  toggle_btn.forEach((toggle_btn) => {
    toggle_btn.addEventListener("click", function () {
      dropmenu.classList.remove("hidden");
      dropmenu.classList.add('animate__fadeInDown');
      document.body.classList.add('overflow-hidden')
    });
  });

  close_btn.addEventListener("click", function () {
    dropmenu.classList.add('animate__fadeOutUp');
    setTimeout(() => {
      dropmenu.classList.add("hidden");
      dropmenu.classList.remove('animate__fadeInDown', 'animate__fadeOutUp');
    }, 300);
    document.body.classList.remove('overflow-hidden')
  });
}

// Share Div
share_links = document.querySelector('.share-div')
share_btn = document.querySelector('.share')
let isShareDivVisible = false;
if (document.querySelector('.share-div')){
    share_btn.addEventListener('click', () => {
      if (isShareDivVisible) {
        share_links.classList.add('animate__fadeOutDown');
        setTimeout(() => {
          share_links.classList.add('hidden');
          share_links.classList.remove('animate__fadeOutDown');
        }, 600);
      } else {
        share_links.classList.remove('hidden');
        share_links.classList.add('animate__fadeInUp');
      }

      isShareDivVisible = !isShareDivVisible;
    });
}

// Notification Tab Function
if (document.querySelectorAll(".noticeToggle")) {
  const toggleButtons = document.querySelectorAll(".noticeToggle");
  const notificationDiv = document.getElementById("notificationDiv");
  toggleButtons.forEach((toggleButton) => {
    toggleButton.addEventListener("click", function () {
      notificationDiv.classList.toggle("active");
      toggleOverlay()
    });
  });
}

if (document.querySelector('.sideMore')){
const sideDivButton = document.querySelector('.sideMore')
const closeSideDivButton = document.querySelector('#closesidemore')
const sideDiv = document.querySelector('#sidemore')

closeSideDivButton.addEventListener('click', ()=> {
    sideDiv.classList.remove('active')
    toggleOverlay()
})
    sideDivButton.addEventListener("click", function () {
      sideDiv.classList.toggle("active");
      toggleOverlay()
    })

// Overlay Feature
const overlay_div = document.querySelector('.overlay')
function toggleOverlay(){
    overlay_div.classList.toggle('hidden')
}
overlay_div.addEventListener('click', ()=> {
    notificationDiv.classList.remove("active");
    sideDiv.classList.remove('active')
    toggleOverlay()
})
}

// Placeholder Animation
const inputFields = document.querySelectorAll(".quiz-input");

function handleInputFocus() {
  const label = this.parentNode.querySelector(".placeholder-label");
  if (this.value) {
    label.classList.add("placeholder-active");
    label.classList.remove("placeholder-not-active");
  } else {
    label.classList.remove("placeholder-active");
    label.classList.add("placeholder-not-active");
  }
}

// Add event listeners to each input field
inputFields.forEach((input) => {
  input.addEventListener("input", handleInputFocus);
});

// Form Transition Effect
if (document.querySelector(".form-step")) {
  const formSteps = document.querySelectorAll(".form-step");
  const nextButtons = document.querySelectorAll(".next-button");
  const previousButtons = document.querySelectorAll(".previous-button");
  let currentStep = 0;

  function navigateToStep(offset) {
    const nextStep = currentStep + offset;
    if (nextStep >= 0 && nextStep < formSteps.length) {
      formSteps[currentStep].classList.add("hidden");
      formSteps[nextStep].classList.remove("hidden");
      formSteps[nextStep].classList.add("animate__fadeInLeft");
      currentStep = nextStep;
    }
  }

  nextButtons.forEach((button) => {
    button.addEventListener("click", () => navigateToStep(1));
  });

  previousButtons.forEach((button) => {
    button.addEventListener("click", () => navigateToStep(-1));
  });
}

// Appending a new question
if (document.querySelector(".completed_questions")) {
  const add_button = document.getElementById("add_question");

  const container = document.querySelector(".write");
  function addNewQuestion() {
    const new_question =
      "<div class='mt-3 relative'> <label class='placeholder-label bg-white'>Question</label> <input class='w-full mt-2 border rounded-md p-2 outline-none focus:border-red quiz-input' type='text' placeholder='' /> </div> <div class='mt-3'> <label class='font-bold'>Options</label><div class='flex gap-3'><i class='lar la-circle my-auto text-grey'></i><input class='w-full mt-2 border rounded-md p-2 outline-none focus:border-red' type='text' placeholder='Option 1' /> </div><div class='flex gap-3'><i class='lar la-circle my-auto text-grey'></i> <input class='w-full mt-2 border rounded-md p-2 outline-none focus:border-red block' type='text' placeholder='Option 2' /></div><div class='flex gap-3'><i class='lar la-circle my-auto text-grey'></i><input class='w-full mt-2 border rounded-md p-2 outline-none focus:border-red block' type='text'placeholder='Option 3' /></div> <div class='flex gap-3'> <i class='lar la-circle my-auto text-grey'></i><input class='w-full mt-2 border rounded-md p-2 outline-none focus:border-red block' type='text' placeholder='Option 4'/></div> </div>";
    container.innerHTML += new_question;
  }
  add_button.addEventListener("click", addNewQuestion);
  const newInputFields = container.querySelectorAll(".quiz-input");
  // Add event listeners to the new input fields
  newInputFields.forEach((input) => {
    input.addEventListener("input", handleInputFocus);
  });
}