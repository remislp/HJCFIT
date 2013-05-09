#include <DCProgsConfig.h>

#include <iostream>
#include "equilibrium.h"
#include "idealg.h"

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
        return {matrix, b};
      } 
  
    // Should work for both IdealG and MissedEventsG.
    // Creates basic input matrix for open and shut cases
    // Retrieves Ax = b problem and solves it using Eigen.
    template<class T> t_initvec equilibrium_impl_(T const &_gmatrix, bool _open) {
        
      std::tuple<t_rmatrix, t_rvector> problem = _open ?
        lstsq_impl_( _gmatrix.laplace_af(0) * _gmatrix.laplace_fa(0) ):
        lstsq_impl_( _gmatrix.laplace_fa(0) * _gmatrix.laplace_af(0) );
    
      return std::get<0>(problem)
                  .jacobiSvd(Eigen::ComputeThinU | Eigen::ComputeThinV)
                  .solve(std::get<1>(problem))
                  .transpose();
    }
  }

  // Untemplates the templates.
  t_initvec equilibrium(IdealG const &_idealg, bool _open) {
    return equilibrium_impl_(_idealg, _open);
  }

}