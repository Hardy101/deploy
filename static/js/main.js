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

// All Menu Function
if (document.getElementById("toggle_btn")) {
  const toggle_btn = document.querySelectorAll(".toggle_btn");
  const dropmenu = document.getElementById("all_menu");
   toggle_btn.forEach((toggle_btn) => {
       toggle_btn.addEventListener("click", function () {
        isOpen = !isOpen;
        dropmenu.classList.toggle("show", isOpen);
        dropmenu.classList.toggle("hide", !isOpen);
      });
   })
}

// Notification Tab Function
if (document.querySelectorAll(".noticeToggle")) {
  const toggleButtons = document.querySelectorAll(".noticeToggle");
  const notificationDiv = document.getElementById("notificationDiv");

  toggleButtons.forEach((toggleButton) => {
    toggleButton.addEventListener("click", function () {
      notificationDiv.classList.toggle("active");
    });
  });
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
