import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 
                      'global_connect.settings')

import django
django.setup()
from studentsconnect.models import Category, Page

def populate():

    python_pages = [
        {'title':'International Student Visa',
         'url':'https://www.gov.uk/student-visa/'},
        {'title': 'International Student Healthcare',
         'url':'https://www.gov.uk/healthcare-immigration-application'},
        {'title':'International Student Housing',
         'url':'https://www.rightmove.co.uk/'},
         {'title': 'International Student Finances',
          'url': 'https://www.ukcisa.org.uk/Information--Advice/Fees-and-Money/Home-or-Overseas-fees-the-basics'}]
    
    django_pages = [
        {'title':'Official Django Tutorial',
         'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/'},
        {'title':'Django Rocks',
         'url':'http://www.djangorocks.com/'},
        {'title':'How to Tango with Django',
         'url':'http://www.tangowithdjango.com/'} ]

    other_pages = [
        {'title':'Bottle',
         'url':'http://bottlepy.org/docs/dev/'},
        {'title':'Flask',
         'url':'http://flask.pocoo.org'} ]

    cats = {'International Student Advice': {'pages': python_pages, 'views': 128, 'likes': 64},
            'Jobs': {'pages': django_pages, 'views': 64, 'likes': 32},
            'Social Wellbeing': {'pages': other_pages, 'views': 32, 'likes': 16} }
    
    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['views'], cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views = 0, likes = 0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

if __name__ == '__main__':
    print('Starting StudentsConnect population script...')
    populate()