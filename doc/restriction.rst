Restrictions
============

Restrictions are special type of Classes in ontology.

Restrictions on a Property
--------------------------

::

   >>> from owlready import *
   
   >>> onto = Ontology("http://test.org/onto.owl")
   
   >>> class Drug(Thing):
   ...     ontology = onto
   
   >>> class ActivePrinciple(Thing):
   ...     ontology = onto
   
   >>> class has_for_active_principle(Property):
   ...     ontology = onto
   ...     domain   = [Drug]
   ...     range    = [ActivePrinciple]

For example, a Placebo is a Drug with no Active Principle:

::

   >>> class Placebo(Drug):
   ...     equivalent_to = [Drug & NOT(restriction(has_for_active_principle, SOME, ActivePrinciple))]

In the example above, 'restriction(has_for_active_principle, SOME, ActivePrinciple)' is the Class of all
objects that have at least one Active Principle. The NOT() function returns the negation of a Class.
The & operator returns the intersection of two Classes.

Another example: an Association Drug is a Drug that associates two or more Active Principle:

::

   >>> class DrugAssociation(Drug):
   ...     equivalent_to = [Drug & restriction(has_for_active_principle, MIN, 2, ActivePrinciple)]

Owlready provides the following types of restrictions (they have the same names than in Protégé):

 * some : restriction(Property Class, SOME, Range Class)
 * only : restriction(Property Class, ONLY, Range Class)
 * min : restriction(Property Class, MIN, cardinality, Range Class)
 * max : restriction(Property Class, MAX, cardinality, Range Class)
 * exactly : restriction(Property Class, EXACTLY, cardinality, Range Class)
 * value : restriction(Property Class, VALUE, Range Instance)


Class operators
---------------

Owlready provides the following operators between Classes (normal Classes but also restrictions):

 * & : and operator (intersection). For example: Class1 & Class2
 * | : or operator (union). For example: Class1 | Class2
 * NOT() : not operator (negation). For example: NOT(Class1)


One Of restrictions
-------------------

In ontologies, a 'One Of' statement is used for defining a Class by extension, *i.e.* by listing its Instances
rather than by defining its properties.

::
   
   >>> class DrugForm(Thing):
   ...     ontology = onto
   
   >>> tablet     = DrugForm()
   >>> capsule    = DrugForm()
   >>> injectable = DrugForm()
   >>> pomade     = DrugForm()

   # Assert that there is only four drug forms possible
   >>> DrugForm.is_a.append(one_of(tablet, capsule, injectable, pomade))
   

