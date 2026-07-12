from django import template

from subscriptions.models import Subscription

register = template.Library()


@register.inclusion_tag("includes/subscription_button.html", takes_context=True)
def subscription_button(context, pet):
    """Кнопка Подписаться/Отписаться на карточке питомца."""
    user = context["request"].user
    can_subscribe = user.is_authenticated and pet.owner_id != user.id
    is_subscribed = can_subscribe and Subscription.objects.filter(user=user, pet=pet).exists()
    return {"pet": pet, "can_subscribe": can_subscribe, "is_subscribed": is_subscribed}
