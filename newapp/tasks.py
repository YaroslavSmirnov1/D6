from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category
import datetime as DT
from datetime import timedelta, date, datetime

import zoneinfo
# pip install backports.zoneinfo

# try:
#     import zoneinfo
# except ImportError:
#     from backports import zoneinfo


MSC = zoneinfo.ZoneInfo("Europe/Moscow")
datetime(2022, 5, 2, tzinfo=MSC)


def weekly_digest():
    categories = Category.objects.all()
    today = DT.datetime.today()
    week = timedelta(days=7)

    print('today', today)

    for category in categories:
        category_subscribers = category.subscribers.all()
        print('category_subscribers', category_subscribers)
        category_subscribers_emails = []
        for subscriber in category_subscribers:
            category_subscribers_emails.append(subscriber.email)
        print('category_subscribers', category_subscribers_emails)

        weekly_posts_in_category = []
        posts_in_category = Post.objects.all().filter(postCategory=f'{category.id}')

        for post in posts_in_category:
            print('today = ', today)
            time_delta = DT.datetime.now() - post.dateCreation
            print('days_delta', days_delta)
            
            if time_delta < week:
                weekly_posts_in_category.append(post)
                print(f'Дата публикации: {post.dateCreation}')
                print(f'Дельта: {time_delta}')
                print('----------------   ---------------')

        print(f'ID: {category.id}')
        print(f'Кол-во публикаций: {len(weekly_posts_in_category)}')
        print(category_subscribers_emails)
        print(weekly_posts_in_category)
        print('----------------   ---------------')
        print('----------------   ---------------')
        print('----------------   ---------------')

        if category_subscribers_emails:
            msg = EmailMultiAlternatives(
                subject=f'Weekly digest for subscribed category "{category}" from News Portal.',
                body=f'Привет! Еженедельная подборка публикаций в выбранной категории "{category}"',
                from_email='anrodion81222@yandex.ru',
                to=category_subscribers_emails,
            )

            # получаем наш html
            html_content = render_to_string(
                'weekly_notify.html',
                {
                    'digest': weekly_posts_in_category,
                    'category': category,
                }
            )

            msg.attach_alternative(html_content, "text/html")  # добавляем html

            msg.send()  # отсылаем
        else:
            continue
