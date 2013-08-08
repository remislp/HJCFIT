**********
User Guide
**********

The likelihood :math:`L` of a sequence of observed open and shut events :math:`\{t_{oi}, t_{si}\}`
can be computed as a series over the missed-events likelihoods for open events,
:math:`{}^e\mathcal{G}_{AF}(t_{oi})` and the missed-events likelihoods for shut events,
:math:`{}^e\mathcal{G}_{FA}(t_{oi})` :cite:`colquhoun:1996`: 

.. _log10likelihood_equation:
.. math::

  L(Q, \{t_{oi}, t_{si}\})
    = \phi_A 
      \left[\prod_i^{n-1}{}^e\mathcal{G}_{AF}(t_{oi}){}^e\mathcal{G}_{AF}(t_{si})\right]
      {}^e\mathcal{G}_{AF}(t_{on}) \phi_e

where :math:`Q` is the transition rate matrix, and :math:`\phi_A` and :math:`\phi_e` are the initial
and final occupancies. All these objects -- as well as their components -- can be accessed both from
python and from c++. In the following, we try and show how they can be created and manipulated from
either language.



.. toctree::
   :maxdepth: 2


   manual/qmatrix.rst
   manual/likelihood_of_Q.rst
   manual/missedeventsG.rst
   manual/occupancies.rst