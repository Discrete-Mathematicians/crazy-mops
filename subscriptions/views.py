from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from pets.models import Pet

from .models import Subscription


@login_required
@require_POST
def subscribe(request, pet_pk):
    pet = get_object_or_404(Pet, pk=pet_pk)
    if pet.owner_id == request.user.id:
        return HttpResponseForbidden()
    Subscription.objects.get_or_create(user=request.user, pet=pet)
    return redirect("pets:detail", pk=pet_pk)


@login_required
@require_POST
def unsubscribe(request, pet_pk):
    pet = get_object_or_404(Pet, pk=pet_pk)
    Subscription.objects.filter(user=request.user, pet=pet).delete()
    return redirect("pets:detail", pk=pet_pk)
