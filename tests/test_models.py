"""Tests for projects models."""
import pytest
from django.utils import timezone

from projects.models import Project


@pytest.mark.django_db
class TestProject:
    """Project model tests."""

    def test_create(self, project):
        """Test Project creation."""
        assert project.pk is not None
        assert project.is_deleted is False

    def test_str(self, project):
        """Test string representation."""
        assert str(project) is not None
        assert len(str(project)) > 0

    def test_soft_delete(self, project):
        """Test soft delete."""
        pk = project.pk
        project.is_deleted = True
        project.deleted_at = timezone.now()
        project.save()
        assert not Project.objects.filter(pk=pk).exists()
        assert Project.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, project):
        """Test default queryset excludes deleted."""
        project.is_deleted = True
        project.deleted_at = timezone.now()
        project.save()
        assert Project.objects.filter(hub_id=hub_id).count() == 0


