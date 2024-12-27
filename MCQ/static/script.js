document.addEventListener("DOMContentLoaded", () => {
  const formFields = document.getElementById("formFields");
  const addInputButton = document.getElementById("addInput");
  const scoreDisplay = document.getElementById("scoreDisplay");

  let totalQuestions = 0;
  let correctAnswersCount = 0;

  // Handle both Add Input and Submit logic
  addInputButton.addEventListener("click", (event) => {
    if (addInputButton.textContent === "Generate MCQ") {
      event.preventDefault();

      // Add the textarea
      const textareaField = document.createElement("div");
      textareaField.className = "mb-3";
      textareaField.innerHTML = `
        <textarea class="form-control" name="text" id="text" rows="3" placeholder="Enter your text here"></textarea>
      `;
      formFields.appendChild(textareaField);

      // Change button text and type
      addInputButton.textContent = "Submit";
      addInputButton.type = "submit"; // Set button to submit form on next click
    }
  });

  // Handle checking of answers for each MCQ
  document.querySelectorAll(".check-answer").forEach((button) => {
    totalQuestions++; // Increment total questions count

    button.addEventListener("click", () => {
      const questionId = button.getAttribute("data-question-id");
      const selectedOption = document.querySelector(
        `input[name="q${questionId}"]:checked`
      );

      if (!selectedOption) {
        alert("Please select an answer.");
        return;
      }

      const userAnswer = selectedOption.value; // Get the selected option
      fetch(`/get-answer/${questionId}`)
        .then((response) => response.json())
        .then((data) => {
          const answerElem = document.getElementById(`answer-${questionId}`);
          if (data.correct_answer) {
            if (userAnswer === data.correct_answer) {
              answerElem.textContent = `Your answer is correct! Correct Answer: ${data.correct_answer}`;
              answerElem.style.color = "green";
              correctAnswersCount++; // Increment correct answers count
            } else {
              answerElem.textContent = `Your answer is incorrect. Correct Answer: ${data.correct_answer}`;
              answerElem.style.color = "red";
            }
            answerElem.style.display = "block";
          } else {
            answerElem.textContent = "Answer not found.";
            answerElem.style.color = "orange";
            answerElem.style.display = "block";
          }
          // Automatically update the score
          updateScore();
        })
        .catch((err) => {
          console.error("Error fetching answer:", err);
          const answerElem = document.getElementById(`answer-${questionId}`);
          answerElem.textContent = "There was an error fetching the answer.";
          answerElem.style.color = "red";
          answerElem.style.display = "block";
        });
    });
  });

  // Update score after each question is answered
  function updateScore() {
    if (totalQuestions > 0) {
      scoreDisplay.textContent = `Your score: ${correctAnswersCount} / ${totalQuestions}`;
      scoreDisplay.style.color = "blue";
    }
  }
});
