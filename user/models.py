from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django_cte import CTEManager

# Create your models here.


class Trips(models.Model):
    user = models.ForeignKey("Users", models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    type = models.SmallIntegerField(blank=True, null=True)
    visibility = models.SmallIntegerField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField()
    last_modified = models.DateTimeField(blank=True, null=True)
    synchronized = models.BooleanField(blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    fb_publish_status = models.SmallIntegerField(blank=True, null=True)
    open_graph_id = models.CharField(max_length=100, blank=True, null=True)
    total_km = models.FloatField(blank=True, null=True)
    likes = models.IntegerField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    quality_score = models.FloatField(blank=True, null=True)
    cover_photo_path = models.CharField(max_length=500, blank=True, null=True)
    uuid = models.TextField(blank=True, null=True)
    cover_photo_thumb_path = models.CharField(max_length=500, blank=True, null=True)
    mashup_user = models.ForeignKey(
        "Users",
        models.DO_NOTHING,
        related_name="trips_mashup_user_set",
        blank=True,
        null=True,
    )
    featured = models.BooleanField(blank=True, null=True)
    feature_text = models.CharField(max_length=500, blank=True, null=True)
    language = models.CharField(max_length=2, blank=True, null=True)
    feature_date = models.DateField(blank=True, null=True)
    creation_time = models.DateTimeField()
    timezone_id = models.CharField(max_length=255, blank=True, null=True)
    summary = models.CharField(max_length=80, blank=True, null=True)
    featured_priority_for_new_users = models.BooleanField(blank=True, null=True)
    planned_steps_visible = models.BooleanField(blank=True, null=True)
    future_timeline_last_modified = models.DateTimeField(blank=True, null=True)
    search_vector = SearchVectorField(null=True)

    objects = CTEManager()

    class Meta:
        db_table = "trips"
        indexes = [GinIndex(fields=["search_vector"])]


class Media(models.Model):
    type = models.SmallIntegerField(blank=True, null=True)
    path = models.CharField(max_length=500, blank=True, null=True)
    step_id = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    is_deleted = models.BooleanField()
    last_modified = models.DateTimeField(blank=True, null=True)
    synchronized = models.BooleanField(blank=True, null=True)
    large_thumbnail_path = models.CharField(max_length=500, blank=True, null=True)
    small_thumbnail_path = models.CharField(max_length=500, blank=True, null=True)
    md5 = models.CharField(max_length=255, blank=True, null=True)
    uuid = models.TextField(blank=True, null=True)
    order = models.SmallIntegerField(blank=True, null=True)
    full_res_unavailable = models.BooleanField()
    full_res_width = models.FloatField(blank=True, null=True)
    full_res_height = models.FloatField(blank=True, null=True)
    aspect_ratio = models.FloatField(blank=True, null=True)
    backup_uploaded = models.BooleanField(blank=True, null=True)
    duration = models.BigIntegerField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    point = models.TextField(blank=True, null=True)  # This field type is a guess.
    geolocation_from_step = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = "media"


class Locations(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    detail = models.CharField(max_length=100, blank=True, null=True)
    is_deleted = models.BooleanField(blank=True, null=True)
    last_modified = models.DateTimeField(blank=True, null=True)
    synchronized = models.BooleanField(blank=True, null=True)
    full_detail = models.CharField(max_length=200, blank=True, null=True)
    venue = models.CharField(max_length=255, blank=True, null=True)
    uuid = models.TextField(blank=True, null=True)
    country_code = models.CharField(max_length=3, blank=True, null=True)
    accuracy = models.FloatField(blank=True, null=True)
    precision = models.FloatField(blank=True, null=True)
    elevation = models.FloatField(blank=True, null=True)
    point = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        db_table = "locations"


class Steps(models.Model):
    trip = models.ForeignKey("Trips", models.DO_NOTHING, blank=True, null=True)
    location = models.ForeignKey(Locations, models.DO_NOTHING, blank=True, null=True)
    description = models.CharField(max_length=100000, blank=True, null=True)
    type = models.SmallIntegerField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField()
    last_modified = models.DateTimeField(blank=True, null=True)
    synchronized = models.BooleanField(blank=True, null=True)
    main_media_item_path = models.CharField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    creation_time = models.DateTimeField(blank=True, null=True)
    zelda_step_id = models.IntegerField(blank=True, null=True)
    timezone_id = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    fb_publish_status = models.SmallIntegerField(blank=True, null=True)
    open_graph_id = models.CharField(max_length=100, blank=True, null=True)
    likes = models.IntegerField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    uuid = models.TextField(blank=True, null=True)
    db_insertion_time = models.DateTimeField()
    facebook_image_url = models.CharField(max_length=500, blank=True, null=True)
    weather_condition = models.CharField(max_length=50, blank=True, null=True)
    weather_temperature = models.FloatField(blank=True, null=True)
    comment_count = models.IntegerField(blank=True, null=True)
    like_count = models.IntegerField(blank=True, null=True)
    spot_count = models.IntegerField(blank=True, null=True)

    objects = CTEManager()

    class Meta:
        db_table = "steps"


class Users(models.Model):
    username = models.CharField(unique=True, max_length=50, blank=True, null=True)
    profile_image_path = models.CharField(max_length=255, blank=True, null=True)
    visibility = models.SmallIntegerField(blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    traveller_type = models.CharField(max_length=100, blank=True, null=True)
    living_location = models.ForeignKey(
        Locations, models.DO_NOTHING, blank=True, null=True
    )
    is_deleted = models.BooleanField()
    last_modified = models.DateTimeField(blank=True, null=True)
    synchronized = models.BooleanField(blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True)
    living_location_name = models.CharField(max_length=255, blank=True, null=True)
    unit_is_km = models.BooleanField()
    quality_score = models.FloatField(blank=True, null=True)
    uuid = models.TextField(blank=True, null=True)
    profile_image_thumb_path = models.CharField(max_length=255, blank=True, null=True)
    mashup_user = models.ForeignKey("self", models.DO_NOTHING, blank=True, null=True)
    temperature_is_celsius = models.BooleanField()
    locale = models.CharField(max_length=32, blank=True, null=True)
    has_multiple_devices = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = "users"


class Images(models.Model):
    id = models.BigAutoField(primary_key=True)
    path = models.CharField(max_length=500, blank=True, null=True)
    step_id = models.IntegerField(blank=True, null=True)
    large_thumbnail_path = models.CharField(max_length=500, blank=True, null=True)
    small_thumbnail_path = models.CharField(max_length=500, blank=True, null=True)
    uuid = models.TextField(blank=True, null=True)
    order = models.SmallIntegerField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = "images"
