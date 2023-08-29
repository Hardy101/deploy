let check = 0
let correctAnswersCount = 0;
que_num_get = document.querySelectorAll('.question_num_get')
que_num_nav = document.querySelector('.question_num')
total_que_num = document.querySelector('.total_que_num')
/*
function checkAnswer(event){
    const clickedOption = event.target;
    parentElement = clickedOption.parentNode;
    is_correct = parentElement.getAttribute('data-answer')=='true'
    correctIndex = correctOption.getAttribute('data-answer')
    if (is_correct){
        clickedOption.classList.add('bg-green','text-white')
    }
    else{
        clickedOption.classList.add('bg-red','text-white')
        correctOption = document.querySelectorAll('.list'+check)
        correctOption.forEach(option => {
            option_attr = option.getAttribute('data-answer')=='true'
            if (option_attr === true){
                option.querySelector('.btn').classList.add('bg-green', 'text-white')
            }
    })
    }
    check+=1
}
*/
function checkAnswer(event) {
    const clickedOption = event.target;
    const parentListItem = clickedOption.closest('li');
    const is_correct = parentListItem.getAttribute('data-answer') === 'true';
    const nextPageLink = document.getElementById('nextPageLink');


  if (is_correct) {
    clickedOption.classList.add('bg-green', 'text-white');
    correctAnswersCount++;
    document.querySelector('#score').textContent = correctAnswersCount;
  } else {
    clickedOption.classList.add('bg-red', 'text-white');

    const correctOption = parentListItem.parentElement.querySelector('[data-answer="true"]');
    if (correctOption) {
      correctOption.querySelector('.btn').classList.add('bg-green', 'text-white');
    }
  }
  nextPageLink.href = `endquiz?score=${correctAnswersCount}`;
}

// Function to toggle class for the current div and the next div
const divs = document.querySelectorAll('.questionDiv');
const buttons = document.querySelectorAll('.btn');
const button = document.querySelector('.btn_next');
const button_prev = document.querySelector('.btn_prev');
let currentQuestion = 0;
divs[currentQuestion].classList.remove('hidden');
total_que_num.textContent = divs.length
buttons.forEach(btn => {
    btn.addEventListener('click', (event) => {
        checkAnswer(event)
    });
});
// ShowQuestion
function showQuestion(questionIndex) {
    divs[currentQuestion].classList.add('hidden');
    divs[questionIndex].classList.remove('hidden');
    divs[questionIndex].classList.add('animate__fadeInLeft');
    currentQuestion = questionIndex;
    que_num_nav.textContent = currentQuestion + 1;
}

// Displaying Next Question
button.addEventListener('click', function(){
 if (currentQuestion < divs.length - 1) {
        showQuestion(currentQuestion + 1);
    }
})

button_prev.addEventListener('click', function() {
    if (currentQuestion > 0) {
        showQuestion(currentQuestion - 1);
    }
});
//Change Question Number in nav


//////////////////////////////////////////
//let countDownDate = new Date().getTime() + 30 * 60000; // 30 minutes from now
//
//let x = setInterval(function () {
//  let now = new Date().getTime();
//  let distance = countDownDate - now;
//
//  let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
//  let seconds = Math.floor((distance % (1000 * 60)) / 1000);
//
//  document.getElementById("timer").innerHTML = minutes + ":" + seconds;
//
//  if (distance < 0) {
//    clearInterval(x);
//    document.getElementById("timer").innerHTML = "EXPIRED";
//  }
//}, 1000);
//document.getElementById("restartButton").addEventListener("click", function () {
//  countDownDate = new Date().getTime() + 30 * 60000; // Reset the countdown to 30 minutes
//});


//===========================//
// Jump to any question
/* function showQuestion(q) {
  let currentQuestionDiv = document.getElementById(
    "question" + currentQuestion
  );
  let nextQuestionDiv = document.getElementById("question" + q);
  currentQuestion = q;
  if (currentQuestionDiv && nextQuestionDiv) {
    currentQuestionDiv.classList.add("hidden");
    nextQuestionDiv.classList.remove("hidden");
  }
}
btns = document.querySelectorAll(".btn");
btns.forEach((btn) => {
  btn.addEventListener("click", () => {
    showNextQuestion(currentQuestion);
  });
});*/