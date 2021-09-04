from django.db import models


class VideoCategory(models.Model):
    category_id = models.PositiveIntegerField(primary_key=True, unique=True)
    image_link = models.TextField()
    title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Videos(models.Model):
    video_id = models.PositiveIntegerField(primary_key=True, unique=True)
    fa_name = models.CharField(max_length=100)
    en_name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    image_link = models.TextField()
    is_active_image = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    min_age = models.IntegerField(default=-1)
    description = models.TextField()
    length = models.IntegerField()
    summary = models.TextField()
    imdb_rating = models.SmallIntegerField(default=4)
    director = models.CharField(max_length=100)
    country_product = models.CharField(max_length=100, null=True)
    is_dubbed = models.BooleanField(default=False)
    is_episode = models.BooleanField(default=False)
    is_childish = models.BooleanField(default=False)
    link = models.TextField()
    is_active_link = models.BooleanField(default=False)
    preview_link = models.TextField(null=True, blank=True)
    is_active_preview = models.BooleanField(default=False)
    category = models.ForeignKey(VideoCategory, on_delete=models.CASCADE, blank=True)
    added_at = models.DateTimeField(auto_now=True, )

    class Meta:
        verbose_name_plural = "Videos"

    def __str__(self):
        if self.is_childish:
            return self.en_name + " => is childish "
        return self.en_name


class VideoActors(models.Model):
    actor_id = models.PositiveIntegerField(primary_key=True, unique=True)
    fa_name = models.CharField(max_length=100)
    en_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    avatar = models.TextField()
    videos = models.ManyToManyField(to=Videos)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Video Actors"

    def __str__(self):
        return self.en_name


class VideoGenres(models.Model):
    genre_id = models.PositiveIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    videos = models.ManyToManyField(to=Videos)

    class Meta:
        verbose_name_plural = "Video Genres"

    def __str__(self):
        return self.name


class VideoImages(models.Model):
    image_id = models.PositiveIntegerField(primary_key=True, unique=True)
    video = models.ForeignKey(Videos, on_delete=models.CASCADE)
    link = models.TextField(null=True)
    is_sticker = models.BooleanField(default=False)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Video Images"

    def __str__(self):
        return self.video.en_name + '=>' + str(self.image_id)
