import re
import json
from django.db import models

class AutomaticSlugModel(models.Model):
    slug = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        self.slug = self.get_slug()
        super(AutomaticSlugModel, self).save(*args, **kwargs)

    def display_name(self):
        raise NotImplementedError('Must be overridden by master class')

    def get_slug(self):
        res = self.display_name().lower()
        res = re.sub('[^A-Za-z0-9\s\\-_]+', '', res).split(' ')
        return '-'.join(res)

    def __str__(self):
      return self.display_name()

    class Meta:
        abstract = True

class ContentType(AutomaticSlugModel):
    name = models.CharField(max_length=50, blank=True, null=True)

    def display_name(self):
        return self.name
    class Meta:
        verbose_name = 'Content Type'
        verbose_name_plural = 'Content Types'

class Outlet(AutomaticSlugModel):
    website = models.URLField(blank=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    def display_name(self):
        return self.name

    def __str__(self):
        return '{0}, {1}'.format(self.name, self.website)

class Author(AutomaticSlugModel):
    outlets = models.ManyToManyField(Outlet)
    generated = models.BooleanField(default=False)
    name = models.CharField(max_length=50, blank=True, null=True)

    def add_outlet(self, outlet):
        if outlet.pk in [o.pk for o in self.outlets.all()]:
            return
        self.outlets.add(outlet)

    def display_name(self):
        return self.name

    def __str__(self):
        return '{0}, {1}'.format(self.name, str(tuple(o.name for o in  self.outlets.all())))

class Category(models.Model):
    slug = models.CharField(max_length=50)
    name = models.CharField(max_length=50, blank=True, null=True)
    aliases = models.CharField(max_length=500, blank=True, null=True)
    available = models.BooleanField(default=False)
    generateable = models.BooleanField(default=False)

    def add_alias(self, alias):
        if alias not in self.aliases:
            self.aliases += ' ' + alias
            self.save()

    def save(self, *args, **kwargs):
        #try:
        return Category.objects.get(aliases__icontains=self.slug)
        #except:
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

def xml_upload_path(instance, filename):
    return 'xml/{0}/{1}/{2}/{3}/{4}.xml'.format(
        instance.content_type.slug,
        instance.outlet.slug,
        instance.category.slug,
        instance.date.strftime('%y-%m'),
        instance.slug
    )

class Document(AutomaticSlugModel):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    date = models.DateTimeField()
    xml = models.FileField(upload_to=xml_upload_path)

    def display_name(self):
        return self.title

    def __str__(self):
        res = self.date.strftime('%Y-%m-%d_%H-%M-%S') + ': '
        res += self.title
        return res

    class Meta:
        abstract = True

class Corpus(Document):
    content_type = models.ForeignKey(ContentType, related_name='contenttype_corpus', on_delete=models.PROTECT)
    outlet = models.ForeignKey(Outlet, related_name='outlet_corpus', on_delete=models.PROTECT)
    category = models.ForeignKey(Category, related_name='category_corpus', on_delete=models.PROTECT)
    author = models.ForeignKey(Author, default=1,  related_name='author_corpus', on_delete=models.PROTECT)

    url = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Corpus'
        verbose_name_plural = 'Corpora'

class GeneratedDocument(Document):
    sentences = None
    content_type = models.ForeignKey(ContentType, related_name='contenttype_generated', on_delete=models.PROTECT)
    outlet = models.ForeignKey(Outlet, related_name='outlet_generated', on_delete=models.PROTECT)
    category = models.ForeignKey(Category, related_name='category_generated', on_delete=models.PROTECT)
    author = models.ForeignKey(Author, related_name='author_generated')

    html_content = models.TextField()
    text_content = models.TextField(default="")
    image_url = models.URLField(blank=True)
    image_credit = models.CharField(max_length=200, blank=True, unique=False)
    original_corpus = models.ForeignKey('Corpus', null=True, on_delete=models.PROTECT)
    views = models.IntegerField(default=0)

    def get_next(self, amount):
        if self.sentences is None:
          self.sentences = self.text_content.split(".")

        res = []
        for sentence in self.sentences:
          if (len(".".join(res)) + len(sentence)) <= amount:
            res.append(sentence)
        print(".".join(res))
        return ".".join(res)

    @property
    def chars_100(self):
        return self.get_next(100)

    @property
    def chars_200(self):
        return self.get_next(200)

    @property
    def chars_500(self):
        return self.get_next(500)

    @property
    def chars_1000(self):
        return self.get_next(1000)

    @property
    def breadcrumbs_json(self):
        crumbs_dict = {
          "@context": "http://schema.org",
          "@type": "BreadcrumbList",
          "itemListElement": [{
            "@type": "ListItem",
            "position": 1,
            "item": {
              "@id": "/".join(self.human_url.split("/")[:3]),
              "name": "News",
            }
          },{
            "@type": "ListItem",
            "position": 2,
            "item": {
              "@id": "/".join(self.human_url.split("/")[:5]),
              "name": self.category.name,
            }
          },{
            "@type": "ListItem",
            "position": 3,
            "item": {
              "@id": "/".join(self.human_url.split("/")[:6]),
              "name": self.title,
            }
          }]
        }
        return json.dumps(crumbs_dict)

    @property
    def sd_json(self):
      sd_dict = {
        "@context": "http://schema.org",
        "@type": "NewsArticle",
        "mainEntityOfPage": {
          "@type": "WebPage",
          "@id": self.human_url
        },
        "headline": self.title,
        "image": [ self.image_url ],
        "datePublished": self.date.isoformat(),
        "dateModified": self.date.isoformat(),
        "author": {
          "@type": "Person",
          "name": self.author.name
        },
        "publisher": {
          "@type": "Organization",
          "name": "The Weekly Output",
          "logo": {
            "@type": "ImageObject",
            "url": "https://pbs.twimg.com/profile_images/983029147332116480/RdzTRLF8_400x400.jpg", # TMP
            "width": 400, "height": 400
          }
        },
        "description": self.description,
        "interactionCount": str(self.views)
      }
      return json.dumps(sd_dict)

    @property
    def human_url(self):
        return "https://www.weekly-output.com/articles/{0}/{1}/".format(
          self.category.slug,
          self.slug
        )

    def save(self, *args, **kwargs):
        super(GeneratedDocument, self).save(*args, **kwargs)

    def increment_views(self):
        self.views += 1
        self.save()

    def display_name(self):
        return self.title

    def __str__(self):
        return '[{0}] Views: {1} | {2}'.format(
            self.date.strftime('%Y-%m-%d_%H-%M-%S'),
            self.views,
            self.title
        )
