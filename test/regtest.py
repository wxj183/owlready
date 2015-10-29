
import unittest

import owlready
from owlready import *

onto_path.append(os.path.dirname(__file__))


NB_ONTO = 0
def new_onto():
  global NB_ONTO
  NB_ONTO += 1
  return Ontology("http://test.org/onto_%s.owl" % NB_ONTO)

class OntoTest(unittest.TestCase):
  def setUp(self): pass

  def test_reasonning_1(self):
    onto = new_onto()
    
    class Pizza     (Thing): ontology = onto
    class Ingredient(Thing): ontology = onto

    class a_pour_ingredient(InverseFunctionalProperty):
      ontology = onto
      domain   = [Pizza]
      range    = [Ingredient]

    class Legume   (Ingredient): pass
    class Tomate   (Legume):     pass
    class Aubergine(Legume):     pass
    class Fromage  (Ingredient): pass
    class Viande   (Ingredient): pass
    class Poisson  (Ingredient): pass
    class Thon     (Poisson):    pass
    
    onto.all_disjoints.append(AllDisjoint(Pizza, Ingredient))
    onto.all_disjoints.append(AllDisjoint(Legume, Fromage, Viande, Poisson))
    onto.all_disjoints.append(AllDisjoint(Tomate, Aubergine))
    
    class PizzaVegetarienne(Pizza):
      is_a = [
        NOT(restriction("a_pour_ingredient", SOME, Viande)) & NOT(restriction("a_pour_ingredient", SOME, Poisson)),
        ]

    class PizzaNonVegetarienne(Pizza):
      equivalent_to = [
        (Pizza & NOT(PizzaVegetarienne)),
        ]
      
    class PizzaAuThon(Pizza):
      is_a = [
        restriction("a_pour_ingredient", SOME, Tomate),
        restriction("a_pour_ingredient", SOME, Fromage),
        restriction("a_pour_ingredient", SOME, Thon),
        restriction("a_pour_ingredient", ONLY, Tomate | Fromage | Thon),
        ]
      
    ma_pizza = Pizza("ma_pizza",
      ontology = onto,
      a_pour_ingredient = [
        Tomate("tomate1"),
        Fromage("fromage1"),
        Thon("thon1"),
        ],
      a_pour_prix = 10.0
      )
    
    onto.sync_reasoner()
    assert issubclass(PizzaAuThon, PizzaNonVegetarienne)
    assert isinstance(ma_pizza   , PizzaNonVegetarienne)


  def test_inverse_prop_1(self):
    onto = new_onto()
    class Obj(Thing):
      ontology = onto
    class prop(Property):
      ontology = onto
      domain   = [Obj]
      range    = [Obj]
    class antiprop(Property):
      ontology = onto
      inverse_property = prop
      
    o1 = Obj()
    o2 = Obj()
    o1.prop.append(o2)
    assert o2 in o1.prop
    assert o1 in o2.antiprop
    
  def test_inverse_prop_2(self):
    onto = new_onto()
    class Obj(Thing):
      ontology = onto
    class prop(FunctionalProperty):
      ontology = onto
      domain   = [Obj]
      range    = [Obj]
    class antiprop(FunctionalProperty):
      ontology = onto
      inverse_property = prop
      
    o1 = Obj()
    o2 = Obj()
    o1.prop = o2
    assert o1.prop == o2
    assert o2.antiprop == o1
    

  def test_annotation1(self):
    onto = new_onto()
    class Obj(Thing): ontology = onto
    
    ANNOTATIONS[Obj][rdfs.comment] = "Test"
    assert(ANNOTATIONS[Obj]["comment"] == ["Test"])
    
  def test_annotation2(self):
    onto = new_onto()
    class Obj(Thing): ontology = onto
    
    ANNOTATIONS[Obj][rdfs.comment, "fr"] = "Med"
    ANNOTATIONS[Obj][rdfs.comment, "fr"] = "Médicament"
    ANNOTATIONS[Obj][rdfs.comment, "en"] = "Drug"
    assert(len(ANNOTATIONS[Obj]) == 2)
    assert(ANNOTATIONS[Obj]["comment", "fr"] == ["Médicament"])
    assert(ANNOTATIONS[Obj]["comment", "en"] == ["Drug"])

  def test_annotation3(self):
    onto = new_onto()
    class Obj(Thing): ontology = onto
    
    ANNOTATIONS[Obj].add_annotation((rdfs.comment, "fr"), "Med")
    ANNOTATIONS[Obj].add_annotation((rdfs.comment, "fr"), "Médicament")
    ANNOTATIONS[Obj].add_annotation((rdfs.comment, "en"), "Drug")
    assert(len(ANNOTATIONS[Obj]) == 3)
    assert(ANNOTATIONS[Obj]["comment", "fr"] == ["Med", "Médicament"])
    assert(ANNOTATIONS[Obj]["comment", "en"] == ["Drug"])
    
    ANNOTATIONS[Obj].del_annotation((rdfs.comment, "fr"), "Med")
    assert(len(ANNOTATIONS[Obj]) == 2)
    assert(ANNOTATIONS[Obj]["comment", "fr"] == ["Médicament"])
    assert(ANNOTATIONS[Obj]["comment", "en"] == ["Drug"])
    
    ANNOTATIONS[Obj].add_annotation((rdfs.comment, "fr"), "Med")
    del ANNOTATIONS[Obj][rdfs.comment, "fr"]
    assert(len(ANNOTATIONS[Obj]) == 1)
    assert(ANNOTATIONS[Obj]["comment", "en"] == ["Drug"])
    
  def test_annotation4(self):
    onto = new_onto()
    class Obj(Thing):               ontology = onto
    class prop(FunctionalProperty): ontology = onto
    o1 = Obj()
    o2 = Obj()
    o1.prop = o2
    
    ANNOTATIONS[o1, prop, o2][rdfs.comment] = "Test"
    assert(ANNOTATIONS[o1, prop, o2]["comment"] == ["Test"])
    
  def test_annotation5(self):
    onto = new_onto()
    class Obj(Thing):            ontology = onto
    class comment2(rdfs.comment): ontology = onto
    
    ANNOTATIONS[Obj]["comment"] = "1"
    ANNOTATIONS[Obj]["comment2"] = "2"
    assert(ANNOTATIONS[Obj]["comment"] == ["1", "2"])
    assert(ANNOTATIONS[Obj]["comment2"] == ["2"])
    
    del ANNOTATIONS[Obj]["comment"]
    assert(len(ANNOTATIONS[Obj]) == 0)
    
    
  def test_annotation6(self):
    onto = Ontology("http://test.org/test_annotations.owl").load()
    
    assert(ANNOTATIONS[onto.C]["comment", "fr"] == ["Teste !"])
    assert(ANNOTATIONS[onto.C]["comment", "en"] == ["test"])
    assert(ANNOTATIONS[onto.D, owl.is_a, onto.C]["comment"] == ["annot"])
    assert(ANNOTATIONS[onto.rel, owl.domain, onto.D]["comment"] == ["dom"])
    assert(ANNOTATIONS[onto.rel, owl.range, onto.C]["comment"] == ["range1", "range2"])
    assert(ANNOTATIONS[onto.i]["comment"] == ["ind"])
    assert(ANNOTATIONS[onto.i, owl.is_a, onto.D]["comment"] == ["ind class"])
    assert(ANNOTATIONS[onto.i, onto.rel, onto.j]["comment"] == ["ind rel"])
    
    onto.base_iri = "http://test.org/test_annotations_gen.owl"; onto.name = "test_annotations_gen"
    onto.save()
    onto.base_iri = "http://drop_it.owl"; onto.name = "drop_it"
    
    onto = Ontology("http://test.org/test_annotations_gen.owl").load() # Reload
    
    assert(ANNOTATIONS[onto.C]["comment", "fr"] == ["Teste !"])
    assert(ANNOTATIONS[onto.C]["comment", "en"] == ["test"])
    assert(ANNOTATIONS[onto.D, owl.is_a, onto.C]["comment"] == ["annot"])
    assert(ANNOTATIONS[onto.rel, owl.domain, onto.D]["comment"] == ["dom"])
    assert(ANNOTATIONS[onto.rel, owl.range, onto.C]["comment"] == ["range1", "range2"])
    assert(ANNOTATIONS[onto.i]["comment"] == ["ind"])
    assert(ANNOTATIONS[onto.i, owl.is_a, onto.D]["comment"] == ["ind class"])
    assert(ANNOTATIONS[onto.i, onto.rel, onto.j]["comment"] == ["ind rel"])

  def test_python_alias_1(self):
    onto = new_onto()
    class Obj(Thing):
      ontology = onto
    class has_for_obj(Property):
      ontology = onto
      domain   = [Obj]
      range    = [Obj]
      
    ANNOTATIONS[has_for_obj]["python_name"] = "obj"
    o = Obj()
    assert o.obj == []
    o.obj.append(Obj())
    assert len(o.obj) == 1
    assert not hasattr(o, "has_for_obj")
    
    
  def test_fusion_class1(self):
    onto = new_onto()
    class C1(Thing): ontology = onto
    class C2(Thing): ontology = onto
    
    o = C1("o")
    o.is_a.append(C2)
    assert(o.is_a == [C1, C2])
    assert(isinstance(o, C1))
    assert(isinstance(o, C2))
    assert(isinstance(o.__class__, owlready._FusionClass))
    
    o2 = o.__class__("o2")
    assert(o2.is_a == [C1, C2])
    assert(isinstance(o2, C1))
    assert(isinstance(o2, C2))
    assert(isinstance(o2.__class__, owlready._FusionClass))
    
    o.is_a.remove(C1)
    assert(o.is_a == [C2])
    assert(not isinstance(o, C1))
    assert(isinstance(o, C2))
    assert(not isinstance(o.__class__, owlready._FusionClass))
    
  def test_fusion_class2(self):
    onto = new_onto()
    class C1(Thing):
      ontology = onto
    class prop(FunctionalProperty):
      ontology = onto
      range    = [int]
    class C2(Thing):
      ontology      = onto
      equivalent_to = [restriction(prop, VALUE, 1)]
    o = C1("o")
    o.prop = 1
    
    onto.sync_reasoner()
    assert(o.is_a == [C1, C2])
    assert(isinstance(o, C1))
    assert(isinstance(o, C2))
    assert(isinstance(o.__class__, owlready._FusionClass))
    
  def test_is_functional_for1(self):
    onto = Ontology("http://www.semanticweb.org/jiba/ontologies/2014/8/test_functional_for.owl").load()
    
    assert     onto.a_pour_b.is_functional_for(onto.A1)
    assert not onto.a_pour_b.is_functional_for(onto.A2)
    
    
if __name__ == '__main__': unittest.main()
  
