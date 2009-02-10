from string import Template

DEFAULT_ATTRS='fontname="Helvetica", fontsize=10.0, labeldistance=1.4'

class Graph(object):
    """
    A set of entities
    """
    def __init__(self,name="Sample Graph"):
        self.name = name.replace(' ','_')
        self.entities = []

    def add_entity(self,entity):
        self.entities.append(entity)

    def __str__(self):
        out = ['digraph %s {    nodesep=0.7\n' % self.name]
        out.extend(map(lambda x: "  %s" % x,self.entities))

        out.append('')
        for e in self.entities:
            out.extend(map(lambda x: "  %s%s" % (e._safe_name(), x), e.relations))
        out.append('}')

        return '\n'.join(out)

# {'Name': (arrowhead, headlabel, arrowtail, taillabel), ...}
RELATION_TYPES = {
'ManyToMany':  ('dot','','dot',''),
'ZeroOneMany': ('none','','dot',''),
'ZeroOrOne':   ('dot','Z','none',''),
'OneOrMore':   ('dot','P','none',''),
'OneToN':      ('dot','N','none',''),
'OneToOne':    ('none','','none','')
}
class RelationType(object):
    """
    IDEF1X Relationships
    """

    def __init__(self, type_name, identifying=False, n=None):
        if type_name not in RELATION_TYPES.keys():
            raise Error
        if type_name is 'OneToN':
            if n is None:
                raise Error
            self.n = n
        self.rtype = type_name
        self.identifying = identifying

    def __str__(self):
        if self.rtype is 'OneToN':
            ahead, lhead, atail, ltail = RELATION_TYPES['OneToN']
            s = 'arrowhead=%s, headlabel="%s", arrowtail=%s, taillabel="%s"' % \
                (ahead,self.n,atail,ltail)
        else:
            s = 'arrowhead=%s, headlabel="%s", arrowtail=%s, taillabel="%s"' % \
                                                    RELATION_TYPES[self.rtype]
        return '%s%s' % (not self.identifying and 'style="dashed", ' or '', s)


class Relation(object):
    """
    A relation between entities
    """
    
    def __init__(self, name, target_entity, target_namespace="", rtype=None):
        self.name = name
        self.target_namespace = target_namespace
        self.target_entity = target_entity
        self.rtype = rtype
    
    def _target_name(self):
        return "%s_%s" % (self.target_namespace, self.target_entity)

    def __str__(self):
        rt = Template(' -> ${target} [label="${name}", ${attrs}];')
        return rt.substitute({
            'target': self._target_name(),
            'name': self.name.replace(' ','\ '),
            'attrs': '%s, %s' % (str(self.rtype), DEFAULT_ATTRS)})


class Entity(object):
    """
    Any person, place, thing, event or conecpt about which information is kept
    """

    def __init__(self,name,namespace='',pks=[], dependent=False):
        self.namespace = namespace
        self.name = name
        self.pks = pks
        self.dependent = dependent
        
        self.attributes = []
        self.relations = []

        # Django-specific abstract base classes
        self.abstracts = []
        self.abstract_attributes = []


    def add_relation(self, relation):
        self.relations.append(relation)

    def add_attribute(self, attribute):
        self.attributes.append(attribute)

    def _safe_name(self):
        return "%s_%s" % (self.namespace, self.name)

    def __str__(self):
        from string import Template
        t = Template('${name} [shape=${type}, label="{[${name2}]\r${pks}|${attrs}}", ${extra_attrs}];')
        attrs = self.attributes and sorted(self.attributes) or ['']
        out = [t.substitute({
            'name':self._safe_name(),
            'name2':self.name,
            'type':self.dependent and "Mrecord" or "record",
            'pks': '\l'.join(self.pks) + "\l",
            'attrs': '\l'.join(attrs) + "\l",
            'extra_attrs': DEFAULT_ATTRS})]
        return '\n'.join(out)


if __name__=="__main__":
    g = Graph()

    e = Entity('sweet',dependent=True)
    c = Entity('cool')
    b = Entity('okay')

    e.add_relation(Relation('well','cool',rtype=RelationType('ZeroOrOne')))
    e.add_relation(Relation('also means','cool',rtype=RelationType('OneOrMore')))
    b.add_relation(Relation('','sweet',rtype=RelationType('ManyToMany',
        identifying=False)))
    e.add_attribute('hey')
    e.add_attribute('awesome')
    e.pks = ['dude']
    g.add_entity(e)
    g.add_entity(c)
    g.add_entity(b)

    print str(g)

    
