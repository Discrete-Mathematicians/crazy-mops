from django import template
from django.db.models import Count
from django.urls import reverse

from reactions.models import Reaction

register = template.Library()


@register.inclusion_tag('includes/reaction_widget.html')
def reaction_widget(user, post=None, comment=None):
    target = {'post': post, 'comment': None} if post else {'post': None, 'comment': comment}
    counts = dict(
        Reaction.objects
        .filter(**target)
        .values_list('reaction_type')
        .annotate(count=Count('id'))
    )
    user_reaction = None
    if user.is_authenticated:
        existing = Reaction.objects.filter(user=user, **target).first()
        if existing:
            user_reaction = existing.reaction_type

    if post:
        action_url = reverse('reactions:react_post', args=[post.pk])
    else:
        action_url = reverse('reactions:react_comment', args=[comment.pk])

    return {
        'user': user,
        'action_url': action_url,
        'reactions': [
            {
                'code': code,
                'label': label,
                'emoji': Reaction.REACTION_EMOJI[code],
                'count': counts.get(code, 0),
                'is_active': code == user_reaction,
            }
            for code, label in Reaction.REACTION_CHOICES
        ],
    }
    