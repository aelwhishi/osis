from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
from entity.models.entity_year import EntityYear


@login_required
def entities_year(request, entity_version_id):
    entity_year = get_object_or_404(EntityYear, pk=entity_version_id)
    entities_year = entity_year.entity.entityyear_set.select_related("academic_year")
    return render(request, "entity/versions.html", {'obj': entity_year, 'entities_year': entities_year})


@login_required
def entity_read(request, entity_version_id):
    entity_year = get_object_or_404(EntityYear, pk=entity_version_id)

    return render(request, "entity/identification.html", {'obj': entity_year})
