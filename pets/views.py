from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PetForm
from .models import Pet


@login_required
def pet_list(request):
    pets = Pet.objects.filter(owner=request.user)
    return render(request, 'pets/pet_list.html', {'pets': pets})


@login_required
def pet_add(request):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            return redirect('pet_list')
    else:
        form = PetForm()
    return render(request, 'pets/pet_form.html', {'form': form})