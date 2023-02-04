from django.db import models

from webapp.validate.validate_fields import MinLengthValidator


class Article(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='Заголовок',
                             validators=(MinLengthValidator(5),))
    text = models.TextField(max_length=3000, null=False, blank=False, verbose_name='Текст',
                            validators=(MinLengthValidator(5),))
    author = models.CharField(max_length=40, null=False, blank=False, default='Unknown', verbose_name='Автор',
                              validators=(MinLengthValidator(5),))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    tags = models.ManyToManyField('webapp.Tag', related_name='articles', blank=True)

    def __str__(self):
        return "{}. {}".format(self.pk, self.title)


class Comment(models.Model):
    article = models.ForeignKey('webapp.Article', related_name='comments', on_delete=models.CASCADE,
                                verbose_name='Статья')
    text = models.TextField(max_length=400, verbose_name='Комментарий')
    author = models.CharField(max_length=40, null=True, blank=True, default='Аноним', verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')

    def __str__(self):
        return self.text[:20]


class Tag(models.Model):
    name = models.CharField(max_length=31, verbose_name='Тег')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return self.name


class ArticleTag(models.Model):
    article = models.ForeignKey('webapp.Article', related_name='article_tags', on_delete=models.CASCADE,
                                verbose_name='Статья')
    tag = models.ForeignKey('webapp.Tag', related_name='tag_articles', on_delete=models.CASCADE, verbose_name='Тег')

    def __str__(self):
        return f'{self.article} | {self.tag}'
