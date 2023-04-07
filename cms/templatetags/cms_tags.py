from django import template

from libra.models import (Book)

register = template.Library()

@register.inclusion_tag('cms/tags/book-inline-card.html')
def book_card_inline(book: Book):
  copies = book.get_copies()
  context = {
    'book': book,
    'available': bool(copies),
    'copies': copies
  }
  return context