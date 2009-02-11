#!/usr/bin/env python
"""
Todo:
Change 'open' to scheduled in ERD

"""
from django.contrib.admin.views.decorators import staff_member_required
from django.db import models
from django.db.models import get_models
from django.template import RequestContext
from django.contrib.admindocs import utils
from django.shortcuts import render_to_response, Http404
from django.db.models.fields.related import \
    ForeignKey, OneToOneField, ManyToManyField



def django_db_fields(model):
    """
    Return the fields actually stored for each table
    """

    all_fields = set(model._meta.fields)
    for cls in model.__bases__:
        if getattr(cls,'_meta',None):
            all_fields = all_fields.difference(set(cls._meta.fields))
    return all_fields

def django_db_fields_source_order(model):
    
    r = []
    source_order = model._meta.fields
    db_fields = django_db_fields(model)
    for f in source_order:
        if f in db_fields:
            r.append(f)
    return r


def django_field_to_role(f):
    if isinstance(f, ManyToManyField):
        return 'FK'
    elif isinstance(f, ForeignKey):
        if f.primary_key:
            return 'PK & FK'
        else:
            return 'FK'
    elif f.primary_key:
        return 'PK'
    else:
        return '-'

@staff_member_required
def generate_docs(request,app='tiger'):
    """
    Generate documentation from the models in the specified app
    """
    #try:
    model_set = get_models(models.get_app(app))
    #except:
    #    return Http404
        
    context = {}
    context['models'] = []
    for model in model_set:
        m = {}
        m['name'] = model.__name__
        m['attrs'] = []
        m['desc'] = utils.parse_rst(
            utils.parse_docstring(model.__doc__ or '')[0],'')
        for f in django_db_fields_source_order(model):            
            m['attrs'].append({
                    'name':f.name,
                    'type':f.db_type(),
                    'null':f.null and 'NULL' or 'NOT NULL',
                    'desc':f.help_text or f.verbose_name,
                    'role':django_field_to_role(f)})
                    
        context['models'].append(m) 
                   
    return render_to_response('model_docs.html',
        context_instance=RequestContext(request, context))
        
        
