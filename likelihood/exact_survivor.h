/***********************
    DCProgs computes missed-events likelihood as described in
    Hawkes, Jalali and Colquhoun (1990, 1992)

    Copyright (C) 2013  University College London

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
************************/

#ifndef DCPROGS_LIKELIHOOD_EXACT_SURVIVOR_H
#define DCPROGS_LIKELIHOOD_EXACT_SURVIVOR_H

#include <DCProgsConfig.h>

#include <tuple>
#include <map>
#include <vector>
#include <memory>

#include "qmatrix.h"
#include "recursion_formula.h"

namespace DCProgs {

  class ExactSurvivor;

  //! Dumps object to stream.
  MSWINDOBE std::ostream & operator<< (std::ostream &, ExactSurvivor const &);

  //! \brief Implementation of recursion for exact missed-event survivor function
  //! \details Implements the exact-missed event probability calculations, as detailed in Hawkes,
  //! Jalali, and Colquhoun (1990). Specifically, this is equation 3.2.
  class MSWINDOBE ExactSurvivor {
    friend MSWINDOBE std::ostream & operator<< (std::ostream &, ExactSurvivor const &);
    public:
      //! Initializes exact survivor functor.
      //! \param[in] _qmatrix Partitioned matrix with open states in top left corner.
      //! \param[in] _tau Missed event cutoff time.
      ExactSurvivor(QMatrix const &_qmatrix, t_real _tau) { set(_qmatrix, _tau); }
      //! Initializes exact survivor functor.
      //! \param[in] _qmatrix A transition matrix with open states in top left corner
      //! \param[in] _nopen Number of open states. 
      //! \param[in] _tau Missed event cutoff time.
      template<class T>
        ExactSurvivor(Eigen::DenseBase<T> const &_qmatrix, t_uint _nopen, t_real _tau)
          { set(QMatrix(_qmatrix, _nopen), _tau); }
      //! Move constructor
      ExactSurvivor   (ExactSurvivor &&_c) 
                    : recursion_af_(std::move(_c.recursion_af_)),
                      recursion_fa_(std::move(_c.recursion_fa_)),
                      tau_(_c.tau_) {}

      //! Sets the values for which to compute exact g.
      void set(QMatrix const &_qmatrix, t_real _tau);

      //! Probability of no shut times detected between 0 and t.
      t_rmatrix af(t_real t) const;
      //! Probability of no open times detected between 0 and t.
      t_rmatrix fa(t_real t) const;

      //! Gets the value of tau;
      t_real get_tau() const { return tau_; }
  
      //! Returns recursion matrix for af
      t_rmatrix recursion_af(t_uint _i, t_uint _m, t_uint _l) const;
      //! Returns recursion matrix for af
      t_rmatrix recursion_fa(t_uint _i, t_uint _m, t_uint _l) const;
      //! Returns Di  matrix for af
      t_rmatrix D_af(t_uint _i) const;
      //! Returns Di matrix for af
      t_rmatrix D_fa(t_uint _i) const;
      //! Returns eigenvalues for af matrix
      t_rvector eigenvalues_af() const;
      //! Returns eigenvalues for fa matrix
      t_rvector eigenvalues_fa() const;

      //! Move assignment.
      ExactSurvivor& operator=(ExactSurvivor &&_c);

    protected:
      //! \cond 
      // See outside definition
      class MSWINDOBE RecursionInterface;
      //! \endcond 

#     ifndef HAS_CXX11_UNIQUE_PTR
        //! Type of the pointers holding recursion interfaces.
        typedef std::auto_ptr<RecursionInterface> t_RecursionPtr;
#     else
        //! Type of the pointers holding recursion interfaces.
        typedef std::unique_ptr<RecursionInterface> t_RecursionPtr;
#     endif
      //! Pointer to AF recursion interface
      t_RecursionPtr recursion_af_;
      //! Pointer to FA recursion interface
      t_RecursionPtr recursion_fa_;
      //! Max length of missed events.
      t_real tau_;
  };


  //! \brief Implementation of recursion for exact missed-event Survivor function
  //! \details This is an interface to the function recursion_formula.  In practice, this object
  //!          needs not be called directly. Rather the public interface (which is about
  //!          computing the likelihood for an event of duration t) is in the containing class
  //!          ExactSurvivor.
  class MSWINDOBE ExactSurvivor::RecursionInterface {
  
    public:
      //! Element on which to perform recursion.
      typedef t_rmatrix t_element;
      //! Constructor. 
      //! \param[in] _qmatrix The transition state matrix for which to compute
      //!                     \f$^eR_{AF}(t\rightarrow\infty)\f$
      //! \param[in] _tau Maximum length of missed events
      //! \param[in] _doAF Whether to do AF (true) or FA
      RecursionInterface(QMatrix const & _qmatrix, t_real _tau, bool _doAF=true);
  
      //! Recursion element i, m, l.
      t_element operator()(t_uint _i, t_uint _m, t_uint _l);
  
      //! Returns D values.
      t_element const & getD(t_uint _i) const {
        assert(_i <= nbeigvals());
        return dvalues_[_i]; 
      }
      //! Returns i\f$^{th}\f$ eigenvalue.
      t_real get_eigvals(t_uint _i) const {
        assert(_i <= nbeigvals());
        return eigenvalues_(_i);
      }
      //! Returns the number of eigenvalues
      t_uint nbeigvals() const { return static_cast<t_uint>(eigenvalues_.size()); }

      //! Reference to eigenvalues
      t_rvector const & eigenvalues() const { return eigenvalues_; }
      //! A null matrix of appropriate size
      decltype(t_rmatrix::Zero(1,1)) zero() const { return t_rmatrix::Zero(nopen, nopen); };

    protected:
  
      //! Key of the map where coefficient matrices are stored.
      typedef std::tuple<t_uint, t_uint, t_uint> t_key;
      //! Map where coefficients are stored.
      std::map<t_key, t_element> coeff_map_;
      //! D matrices (See equation 3.16)
      std::vector<t_element> dvalues_;
      //! Eigenvalues of the transition rate matrix.
      t_rvector eigenvalues_;
      //! Number of open states.
      t_uint nopen;
  };
}

#endif 

