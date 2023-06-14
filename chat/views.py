from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from . import decorators, chat_func

@csrf_exempt
def home(request):
    if request.method == 'POST':
        key = request.POST['key']
        if decorators.validate_api_key(key):
            request.session['api_key'] = key
            return redirect('chat')
        else:
            messages.info(request, 'Invalid API key')
            return redirect('home')
    else:
        return render(request, 'home.html')

@decorators.validate_api_key
def chat(request):
    if request.method == 'POST':
        if 'message' in request.POST:
            prompt = request.POST['message']
            response = chat_func.valid(prompt)
            context = {
                'prompt': prompt,
                'response': response
            }
            return render(request, 'chat.html', context)
    else:
        # Handle GET request
        return render(request, 'chat.html')
