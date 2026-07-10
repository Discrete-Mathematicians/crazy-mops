from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render


def profile_detail(request, pk):
    User = get_user_model()
    profile_user = get_object_or_404(User, pk=pk)

    pets = profile_user.pets.all()

    can_manage = request.user.is_authenticated and (request.user == profile_user or request.user.is_staff)

    context = {
        "profile_user": profile_user,
        "pets": pets,
        "can_manage": can_manage,
    }
    return render(request, "profiles/profile_detail.html", context)
