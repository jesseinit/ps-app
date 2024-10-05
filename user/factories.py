import factory
from faker import Faker
import pytz
import uuid

fake = Faker()


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "user.Locations"

    name = factory.Faker("city")
    lat = factory.Faker("latitude")
    lon = factory.Faker("longitude")
    detail = factory.Faker("sentence", nb_words=5)
    is_deleted = factory.Faker("boolean")
    last_modified = factory.Faker("date_time_this_year", tzinfo=pytz.UTC)
    synchronized = factory.Faker("boolean")
    full_detail = factory.Faker("sentence", nb_words=4)
    venue = factory.Faker("company")
    uuid = factory.Faker("uuid4")
    country_code = factory.Faker("country_code")
    accuracy = factory.Faker("pyfloat", left_digits=2, right_digits=6, positive=True)
    precision = factory.Faker("pyfloat", left_digits=2, right_digits=6, positive=True)
    elevation = factory.Faker("pyfloat", left_digits=3, right_digits=2)
    point = factory.Faker("text", max_nb_chars=255)


class UsersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "user.Users"

    username = factory.Faker("uuid4")
    profile_image_path = factory.Faker("file_path", depth=3, extension="jpg")
    visibility = factory.Faker("random_int", min=0, max=10)
    description = factory.Faker("text", max_nb_chars=1000)
    traveller_type = factory.Faker("word")
    living_location = factory.SubFactory(LocationFactory)
    is_deleted = factory.Faker("boolean")
    last_modified = factory.Faker("date_time_this_year", tzinfo=pytz.UTC)
    synchronized = factory.Faker("boolean")
    creation_date = factory.Faker("date_time_this_year", tzinfo=pytz.UTC)
    living_location_name = factory.Faker("city")
    unit_is_km = factory.Faker("boolean")
    quality_score = factory.Faker(
        "pyfloat", left_digits=2, right_digits=2, positive=True
    )
    uuid = factory.Faker("uuid4")
    profile_image_thumb_path = factory.Faker("file_path", depth=3, extension="jpg")
    # mashup_user = factory.SubFactory(UserFactory)  # Self-referencing
    temperature_is_celsius = factory.Faker("boolean")
    locale = factory.Faker("locale")
    has_multiple_devices = factory.Faker("boolean")


class TripsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "user.Trips"

    user = factory.SubFactory(UsersFactory)
    name = factory.Faker("sentence", nb_words=3)
    type = factory.Faker("random_int", min=0, max=5)
    visibility = factory.Faker("random_int", min=0, max=10)
    start_date = factory.Faker("date_time_this_year", tzinfo=pytz.UTC)
    end_date = factory.Faker("date_time_this_year", tzinfo=pytz.UTC)
    is_deleted = factory.Faker("boolean")
    last_modified = factory.Faker("date_time_this_year", tzinfo=pytz.UTC)
    synchronized = factory.Faker("boolean")
    slug = factory.Faker("slug")
    fb_publish_status = factory.Faker("random_int", min=0, max=10)
    open_graph_id = factory.Faker("lexify", text="??????????")
    total_km = factory.Faker("pyfloat", left_digits=3, right_digits=2, positive=True)
    likes = factory.Faker("random_int", min=0, max=1000)
    views = factory.Faker("random_int", min=0, max=10000)
    quality_score = factory.Faker(
        "pyfloat", left_digits=1, right_digits=2, positive=True, max_value=5
    )
    cover_photo_path = factory.Faker("file_path", depth=3, extension="jpg")
    uuid = factory.Faker("uuid4")
    cover_photo_thumb_path = factory.Faker("file_path", depth=3, extension="jpg")
    mashup_user = factory.SubFactory(UsersFactory)
    featured = factory.Faker("boolean")
    feature_text = factory.Faker("sentence", nb_words=10)
    language = factory.Faker("random_element", elements=["en", "fr", "es", "de"])
    feature_date = factory.Faker("date_this_year")
    creation_time = factory.Faker("date_time_this_year", tzinfo=pytz.UTC)
    timezone_id = factory.Faker("timezone")
    summary = factory.Faker("sentence", nb_words=4)
    featured_priority_for_new_users = factory.Faker("boolean")
    planned_steps_visible = factory.Faker("boolean")
    future_timeline_last_modified = factory.Faker(
        "date_time_this_year", tzinfo=pytz.UTC
    )

    @factory.post_generation
    def truncate_summary(self, create, extracted, **kwargs):
        # Truncate summary to 80 characters if it exceeds the limit
        if len(self.summary) > 80:
            self.summary = self.summary[:80]


class StepsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "user.Steps"

    trip = factory.SubFactory(TripsFactory)
    location = factory.SubFactory(LocationFactory)
    description = factory.Faker("paragraph", nb_sentences=10)
    type = factory.Faker("random_int", min=0, max=5)
    start_time = factory.Faker("date_time_this_year", tzinfo=pytz.UTC)
    end_time = factory.Faker("date_time_this_year", tzinfo=pytz.UTC)
    is_deleted = factory.Faker("boolean")
    last_modified = factory.Faker("date_time_this_year", tzinfo=pytz.UTC)
    synchronized = factory.Faker("boolean")
    main_media_item_path = factory.Faker("file_path", depth=3, extension="jpg")
    name = factory.Faker("sentence", nb_words=4)
    creation_time = factory.Faker("date_time_this_year", tzinfo=pytz.UTC)
    zelda_step_id = factory.Faker("random_int", min=1, max=1000)
    timezone_id = factory.Faker("timezone")
    slug = factory.Faker("slug")
    fb_publish_status = factory.Faker("random_int", min=0, max=10)
    open_graph_id = factory.Faker("lexify", text="??????????")
    likes = factory.Faker("random_int", min=0, max=1000)
    views = factory.Faker("random_int", min=0, max=10000)
    uuid = factory.Faker("uuid4")
    db_insertion_time = factory.Faker("date_time_this_year", tzinfo=pytz.UTC)
    facebook_image_url = factory.Faker("file_path", depth=3, extension="jpg")
    weather_condition = factory.Faker("word")
    weather_temperature = factory.Faker(
        "pyfloat", left_digits=2, right_digits=1, positive=True
    )
    comment_count = factory.Faker("random_int", min=0, max=500)
    like_count = factory.Faker("random_int", min=0, max=1000)
    spot_count = factory.Faker("random_int", min=0, max=100)


class ImagesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "user.Images"

    id = factory.Sequence(lambda n: n + 1)  # Auto-incrementing id
    path = factory.Faker(
        "file_path", extension="jpg"
    )  # Random file path with '.jpg' extension
    step_id = factory.Faker("random_int", min=1, max=1000)  # Random integer for step_id
    large_thumbnail_path = factory.Faker(
        "file_path", extension="jpg"
    )  # Random large thumbnail path
    small_thumbnail_path = factory.Faker(
        "file_path", extension="jpg"
    )  # Random small thumbnail path
    uuid = factory.LazyFunction(lambda: str(uuid.uuid4()))  # Random UUID as a string
    order = factory.Faker(
        "random_int", min=1, max=100
    )  # Random small integer for order
    lat = factory.Faker("latitude")  # Random latitude
    lon = factory.Faker("longitude")  # Random longitude
