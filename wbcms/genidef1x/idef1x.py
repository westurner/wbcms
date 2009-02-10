#!/usr/bin/env python
from __future__ import with_statement
from django.core.management import setup_environ

try:
    import settings
except ImportError:
    pass
else:
    setup_environ(settings)


from django.utils.safestring import mark_safe
from django.template import Template, Context
from django.db import models
from django.db.models import get_models
from django.db.models.fields.related import \
    ForeignKey, OneToOneField, ManyToManyField
    
try:
    from django.db.models.fields.generic import GenericRelation
except ImportError:
    from django.contrib.contenttypes.generic import GenericRelation    


from erd import Graph, Entity, Relation, RelationType

def is_fk(attr):
    return type(attr) in [ForeignKey, OneToOneField, ManyToManyField]

def django_field_to_relation(f):
    if isinstance(f, ManyToManyField):
        return Relation(f.attname, f.rel.to.__name__,
            f.rel.to.__module__.replace('.','_'),
            RelationType('ManyToMany', f.primary_key))
    elif isinstance(f, OneToOneField):
        return Relation(f.attname, f.rel.to.__name__,
            f.rel.to.__module__.replace('.','_'),
            RelationType('OneToOne', f.primary_key))
    elif isinstance(f, ForeignKey):
        return Relation(f.attname, f.rel.to.__name__,
            f.rel.to.__module__.replace('.','_'),
            RelationType('ZeroOneMany',f.primary_key))

    else:
        raise TypeError

def django_model_to_entity(app,model):
    e = Entity(model.__name__, app.__name__.replace('.','_'),
            [model._meta.pk.attname])

    # Remove duplicate fields from superclass(es)
    
    all_fields = set(model._meta.fields)
    for cls in model.__bases__:
        if getattr(cls,'_meta',None):
            all_fields = all_fields.difference(set(cls._meta.fields))
    
    # Populate Entity with attributes (annotate with "(FK)" as appropriate)
    for f in filter(lambda x: (x.attname not in e.pks) or (x.primary_key), all_fields):
        fk = is_fk(f)
        if not f.primary_key:
            e.add_attribute('%s%s' % (f.attname, fk and ' (FK)' or ''))
        # field_type = type(f).__name__
        if fk:
            e.add_relation(django_field_to_relation(f))

    # Add Relations for ManyToMany fields (xxx: draw bridge table)
    if getattr(model,'_meta',None) and model._meta.many_to_many:
        for f in model._meta.many_to_many:
            e.add_relation(django_field_to_relation(f))
    
    # Return the entity
    return e

def generate_idef1x(app_labels,graph_name='Testing Graph',
    filename=None):
    """
    Generate IDEF1X models with GraphViz from a list of Django application names
    """
    apps = map(lambda x: models.get_app(x), app_labels)

    g = Graph(graph_name)
    
    for app in apps:
        for model in get_models(app):
            g.add_entity(django_model_to_entity(app,model))
    
    with file(filename, 'wb') as f:
        f.writelines(str(g))
          
    

def main():
    from optparse import OptionParser
    arg = OptionParser()
    arg.add_option('--apps',dest='app_labels',
        help='List of applications to graph')
    arg.add_option('--all',dest='all_apps',
        help='Graph all models in all applications')
    arg.add_option('-o','--output',dest='output_file',
        help='File DOT will be written to')
        
    (opts,args) = arg.parse_args()
    
    if opts.app_labels:
        generate_idef1x([opts.app_labels], filename=opts.output_file or 'output.dot')
    

if __name__=="__main__":
    main()
