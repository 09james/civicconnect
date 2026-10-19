"""Seed the initial service request categories."""

from django.db import migrations


def seed_categories(apps, schema_editor):
    category_model = apps.get_model("requests", "Category")
    category_model.objects.bulk_create(
        [
            category_model(name="Street lighting", description="Broken or faulty streetlights"),
            category_model(name="Water supply", description="Leaks, outages, or water quality"),
            category_model(name="Garbage collection", description="Missed pickup or illegal dumping"),
        ],
        ignore_conflicts=True,
    )


def remove_seed_categories(apps, schema_editor):
    category_model = apps.get_model("requests", "Category")
    category_model.objects.filter(
        name__in=("Street lighting", "Water supply", "Garbage collection")
    ).delete()


class Migration(migrations.Migration):
    """Load initial request categories."""

    dependencies = [("requests", "0001_initial")]
    operations = [
        migrations.RunPython(seed_categories, remove_seed_categories),
    ]
