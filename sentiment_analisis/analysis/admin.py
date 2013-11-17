from django.contrib import admin
from analysis.models import Feed, Keyword, Worker, Task, Sentiment
# Register your models here.


admin.site.register(Feed)
admin.site.register(Keyword)
admin.site.register(Worker)
admin.site.register(Task)
admin.site.register(Sentiment)
