
from contact.forms import ContactForm
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
# Create your views here.
from django.contrib import messages
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'your request have been successfully submited ')
            return redirect('contactus')
        else:
            return render(request, 'contact.html', {'form': form})
    else:
        form = ContactForm()
        return render(request, 'contact.html', {'form': form, })
