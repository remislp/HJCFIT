// Starts the likelihood sub-package
%module likelihood
// C++ definitions that are needed to compile the python bindings.
%{
#define SWIG_FILE_WITH_INIT
#  include <DCProgsConfig.h>
#  include <iostream>
#  include <sstream>

#  if NUMPY_VERSION_MINOR >= 7 
#    define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#  endif
#  include <numpy/arrayobject.h>
#  ifndef DCPROGS_NPY_ARRAY
#    define NPY_ARRAY_C_CONTIGUOUS NPY_C_CONTIGUOUS 
#    define NPY_ARRAY_WRITEABLE    NPY_WRITEABLE
#  endif
#  ifndef DCPROGS_NPY_ENABLEFLAGS
#    define PyArray_ENABLEFLAGS(ARRAY, FLAGS)  (ARRAY)->flags |= FLAGS
#    define PyArray_CLEARFLAGS(ARRAY, FLAGS)   (ARRAY)->flags &= (!FLAGS)
#    define PyArray_SetBaseObject(ARRAY, BASE) (ARRAY)->base   = BASE
#  endif
#  include "numpy_eigen.h"

#  include "../state_matrix.h"
#  include "../idealg.h"
#  include "../equilibrium.h"
#  include "../determinant_equation.h"
#  include "../root_finder.h"
#  include "../asymptotes.h"
#  include "../exact_survivor.h"
#  include "../approx_survivor.h"
#  include "../missed_eventsG.h"

#  include "helpers.h"

#ifdef DCPROGS_CATCH
# error DCPROGS_CATCH already defined.
#endif 
#define DCPROGS_CATCH(ONERROR)                                                 \
    catch (DCProgs::errors::ComplexEigenvalues &_e) {                          \
      PyErr_SetString(PyExc_ArithmeticError, _e.what());                       \
      ONERROR;                                                                 \
    } catch (DCProgs::errors::NaN &_e) {                                       \
      PyErr_SetString(PyExc_ArithmeticError, _e.what());                       \
      ONERROR;                                                                 \
    } catch (DCProgs::errors::Mass &_e) {                                      \
      PyErr_SetString(PyExc_ArithmeticError, _e.what());                       \
      ONERROR;                                                                 \
    } catch (DCProgs::errors::Domain &_e) {                                    \
      PyErr_SetString(PyExc_ArithmeticError, _e.what());                       \
      ONERROR;                                                                 \
    } catch (DCProgs::errors::Math &_e) {                                      \
      PyErr_SetString( PyExc_ArithmeticError,                                  \
                       ( std::string("Math error in dcprogs: ")                \
                         + _e.what()).c_str() );                               \
      ONERROR;                                                                 \
    } catch (DCProgs::errors::Index &_e) {                                     \
      PyErr_SetString(PyExc_IndexError, _e.what());                            \
      ONERROR;                                                                 \
    } catch (DCProgs::errors::PythonTypeError &_e) {                           \
      PyErr_SetString(PyExc_TypeError, _e.what());                             \
      ONERROR;                                                                 \
    } catch (DCProgs::errors::PythonValueError &_e) {                          \
      PyErr_SetString(PyExc_ValueError, _e.what());                            \
      ONERROR;                                                                 \
    } catch (DCProgs::errors::PythonErrorAlreadyThrown &) {                    \
      ONERROR;                                                                 \
    } catch (DCProgs::errors::Python &_e) {                                    \
      PyErr_SetString(PyExc_RuntimeError, _e.what());                          \
      ONERROR;                                                                 \
    } catch(DCProgs::errors::NotImplemented &_e) {                             \
      PyErr_SetString(PyExc_NotImplementedError, _e.what());                   \
      ONERROR;                                                                 \
    } catch(DCProgs::errors::Root &_e) {                                       \
      PyErr_SetString( PyExc_RuntimeError,                                     \
                       (std::string("Encountered unknonw error in DCProgs\n")  \
                        + _e.what()).c_str() );                                \
      ONERROR;                                                                 \
    } catch(std::exception &_e) {                                              \
      PyErr_SetString(PyExc_RuntimeError, _e.what());                          \
      ONERROR;                                                                 \
    } catch(...) {                                                             \
      PyErr_SetString(PyExc_RuntimeError, "Caught unknown exception.");        \
      ONERROR;                                                                 \
    }
%}

// Tells swig that we will deal with execptions.
%include "exception.i"
%init %{ import_array();  %}

%exception {
  try { $function }
  DCPROGS_CATCH(return NULL;);
}

// Tells swig about our type hierarchy. 
// These types should make it easier to go from one system to another, but they do make it slightly
// more difficult for swig to understand our code.
%apply int { t_int }; 
%apply int { DCProgs::t_int }; 
%apply double { t_real }; 
%apply double { DCProgs::t_real }; 
%typemap(typecheck) DCProgs::t_int = int;
%typemap(typecheck) t_int = int;
%typemap(typecheck) DCProgs::t_real = double;
%typemap(typecheck) t_real = double;
%typemap(out) DCProgs::t_rvector { 
  try { $result = DCProgs::numpy::wrap_to_numpy($1); }
  DCPROGS_CATCH(SWIG_fail);
}
%typemap(out) DCProgs::t_initvec { 
  try { $result = DCProgs::numpy::wrap_to_numpy($1); }
  DCPROGS_CATCH(SWIG_fail);
}
%typemap(out) DCProgs::t_rmatrix { 
  try { $result = DCProgs::numpy::wrap_to_numpy($1); }
  DCPROGS_CATCH(SWIG_fail);
};



// These macros help us translate from C++ exceptions to python exceptions
//! General namespace for all things DCProgs.
namespace DCProgs {

%include "state_matrix.swg"
%include "idealg.swg"
%include "determinant_equation.swg"
%include "root_finder.swg"
%include "asymptotes.swg"
%include "exact_survivor.swg"
%include "approx_survivor.swg"
%include "missed_eventsG.swg"

}
#undef DCPROGS_CATCH
