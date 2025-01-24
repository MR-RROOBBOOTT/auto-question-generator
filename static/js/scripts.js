document.addEventListener('DOMContentLoaded', () => {
    const generateButton = document.getElementById('generateButton');
    const questionsContainer = document.getElementById('questionsContainer');
    const showAnswersButton = document.createElement('button');
    showAnswersButton.id = 'showAnswersButton';
    showAnswersButton.textContent = 'Show Answer Key';
    showAnswersButton.style.display = 'none'; // Initially hidden
    showAnswersButton.style.marginTop = '20px';

    // Append the button to the container
    questionsContainer.parentNode.appendChild(showAnswersButton);

    generateButton.addEventListener('click', async () => {
        const operator = document.getElementById('operator').value;
        const m = document.getElementById('m').value;
        const n = document.getElementById('n').value;
        const expression = document.getElementById('expression').value;
        const level = document.getElementById('level').value;
        const numQuestions = document.getElementById('numQuestions').value;

        try {
            const response = await fetch(`/generate-question/?operator=${operator}&m=${m}&n=${n}&expression=${encodeURIComponent(expression)}&level=${level}&num_questions=${numQuestions}`);
            const data = await response.json();

            if (!response.ok || data.error) {
                throw new Error(data.error || 'Unknown error occurred.');
            }

            // Clear existing content
            questionsContainer.innerHTML = '';
            showAnswersButton.style.display = 'none'; // Hide the button initially

            // Populate new questions
            data.questions.forEach((q, index) => {
                const questionBlock = document.createElement('div');
                questionBlock.className = 'question-block';
                questionBlock.innerHTML = `
                    <h3>Question ${index + 1}: ${q.question}</h3>
                    <ul>
                        ${q.options.map((opt, optIndex) => `
                            <li data-correct="${opt === q.correct}" style="color: black; font-weight: normal;">${opt}</li>
                        `).join('')}
                    </ul>
                `;
                questionsContainer.appendChild(questionBlock);
            });

            showAnswersButton.style.display = 'inline-block'; // Show the "Show Answer Key" button
        } catch (error) {
            console.error('Error:', error.message || error);
            alert(`Error: ${error.message || 'Failed to generate questions.'}`);
        }
    });

    // Show correct answers when the button is clicked
    showAnswersButton.addEventListener('click', () => {
        const correctAnswers = document.querySelectorAll('[data-correct="true"]');
        correctAnswers.forEach(answer => {
            answer.style.color = 'green'; // Highlight correct answers
            answer.style.fontWeight = 'bold';
        });
        showAnswersButton.disabled = true; // Disable the button after showing the answers
    });
});