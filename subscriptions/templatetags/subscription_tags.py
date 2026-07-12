from django import template

from subscriptions.models import Subscription

register = template.Library()


@register.inclusion_tag('includes/subscription_button.html')
def subscription_button(pet, user):
    """Кнопка подписки на питомца. Свой питомец или гость - кнопки нет."""
    can_subscribe = user.is_authenticated and user != pet.owner
    is_subscribed = (
        can_subscribe
        and Subscription.objects.filter(user=user, pet=pet).exists()
    )
    return {
        'can_subscribe': can_subscribe,
        'pet': pet,
        'is_subscribed': is_subscribed,
    }