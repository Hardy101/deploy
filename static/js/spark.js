let check = 0;
let correctAnswersCount = 0;
que_num_get = document.querySelectorAll(".question_num_get");
que_num_nav = document.querySelectorAll(".question_num");
total_que_num = document.querySelector(".total_que_num");
function checkAnswer(event) {
  const clickedOption = event.target;
  const parentListItem = clickedOption.closest("li");
  const is_correct = parentListItem.getAttribute("data-answer") === "true";
  const nextPageLink = document.getElementById("nextPageLink");

  if (is_correct) {
    clickedOption.classList.add("bg-green", "text-white");
    correctAnswersCount++;
    document.querySelector("#score").textContent = correctAnswersCount;
  } else {
    clickedOption.classList.add("bg-red", "text-white");

    const correctOption = parentListItem.parentElement.querySelector(
      '[data-answer="true"]'
    );
    if (correctOption) {
      correctOption
        .querySelector(".btn")
        .classList.add("bg-green", "text-white");
    }
  }
}

// Function to toggle class for the current div and the next div
const divs = document.querySelectorAll(".questionDiv");
const buttons = document.querySelectorAll(".btn");
const button = document.querySelector(".btn_next");
const button_prev = document.querySelector(".btn_prev");
let currentQuestion = 0;
divs[currentQuestion].classList.remove("hidden");
total_que_num.textContent = divs.length;
buttons.forEach((btn) => {
  btn.addEventListener("click", (event) => {
    checkAnswer(event);
  });
});
// ShowQuestion
function showQuestion(questionIndex) {
  divs[currentQuestion].classList.add("hidden");
  divs[questionIndex].classList.remove("hidden");
  currentQuestion = questionIndex;
  que_num_nav.forEach((que_num_nav) => {
    que_num_nav.textContent = currentQuestion + 1;
  });
}

// Displaying Next Question
button.addEventListener("click", function () {
  if (currentQuestion < divs.length - 1) {
    showQuestion(currentQuestion + 1);
  }
});

button_prev.addEventListener("click", function () {
  if (currentQuestion > 0) {
    showQuestion(currentQuestion - 1);
  }
});

//End Quiz button
const nav = document.getElementById('nav')
const main_div = document.getElementById('main_div')
const score_div = document.getElementById('score_div')
const endquiz_btn = document.getElementById('endquiz')
const net_score = document.getElementById('net_score')
const total_que_count = document.getElementById('total_que_count')
const correct_answer = document.getElementById('correct_answer')
const wrong_answer = document.getElementById('wrong_answer')

total_que_count.textContent = total_que_num.textContent

endquiz_btn.addEventListener('click', function(){
    nav.classList.add('hidden')
    score_div.classList.remove('hidden')
    main_div.classList.add('hidden')
    percentage_score = (correctAnswersCount / parseInt(total_que_num.textContent)) * 100
    net_score.textContent = percentage_score
    correct_answer.textContent = correctAnswersCount
    wrong_answer.textContent = parseInt(total_que_num.textContent) - correctAnswersCount

})