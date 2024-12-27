from django.shortcuts import render
from .services import generate_question, get_answer  # Ensure your import is correct

def home(request):
    if request.method == "POST":
        text = request.POST.get('text', '')  # Safely get 'text' from POST data
        if text:  # Check if the input text is not empty
            questions = generate_question(text)  # Call your function to generate questions
            context = {'questions': questions}
            return render(request, 'base.html', context)  # Render the questions with the context
        else:
            error_message = "Please enter some text to generate questions."
            return render(request, 'base.html', {'error_message': error_message})  # Render with error message if no input
    else:
        return render(request, 'base.html')  # Initial form rendering for GET request
