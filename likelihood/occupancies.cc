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

#include <DCProgsConfig.h>

#include <iostream>
#include "occupancies.h"
#include "idealG.h"
#include "missed_eventsG.h"

namespace DCProgs {

  namespace {
    // Creates the input of problem Ax = 0, with sum x_i = 1.
    //   - A matrix, with an additional rows of 1.
    //   - b vector, empty except for last entry. 
    template<class T>
      std::tuple<t_rmatrix, t_rvector> lstsq_impl_(Eigen::DenseBase<T> const &_in) {
  
        assert(_in.rows() == _in.cols());
  
        auto const n = _in.rows();
        t_rmatrix matrix(n+1, n);
        matrix.topRows(n) = t_rmatrix::Identity(n, n) - _in.transpose();
        matrix.row(n) = t_rmatrix::Ones(1, matrix.cols());
        t_rvector b(n+1);
        b.topRows(n) = t_rvector::Zero(n);
        b(n) = 1;
        return std::make_tuple(matrix, b);
      } 
  
    // Should work for both IdealG and MissedEventsG.
    // Creates basic input matrix for open and shut cases
    // Retrieves Ax = b problem and solves it using Eigen.
    template<class T> t_initvec occupancies_impl_(T const &_gmatrix, bool _open) {
        
      std::tuple<t_rmatrix, t_rvector> problem = _open ?
        lstsq_impl_( _gmatrix.laplace_af(0) * _gmatrix.laplace_fa(0) ):
        lstsq_impl_( _gmatrix.laplace_fa(0) * _gmatrix.laplace_af(0) );
    
      Eigen::JacobiSVD<t_rmatrix>
        svd(std::get<0>(problem), Eigen::ComputeThinU|Eigen::ComputeThinV); 
      return svd.solve(std::get<1>(problem)).transpose();
    }

  }

  // \cond
  // Untemplates the templates.
  t_initvec MSWINDOBE occupancies(IdealG const &_idealg, bool _initial) {
    return occupancies_impl_(_idealg, _initial);
  }
  // \endcond

  t_initvec MSWINDOBE occupancies(MissedEventsG const &_missedeventsG, bool _initial) {
    return occupancies_impl_(_missedeventsG, _initial);
  }

  t_initvec MSWINDOBE CHS_occupancies(MissedEventsG const &_G, t_real _tcrit, bool _initial) {
    
    t_rmatrix const Hfa = CHS_matrix_Hfa(_G, _tcrit);
    if(_initial) {
      // \f$\phi_F H_{FA}\f$
      t_initvec const phif_times_Hfa = occupancies(_G, false) * Hfa;
      // \f$\phi_F H_{FA} / \phi_F H_FA u_A\f$
      return phif_times_Hfa / phif_times_Hfa.array().sum();
    } else {
      // \f$H_{FA} u_A\f$
      return Hfa.rowwise().sum();
    }
  }
}
