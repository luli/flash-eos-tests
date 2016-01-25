!!****if* source/Simulation/SimulationMain/LaserSlab/Simulation_data
!!
!! NAME
!!  Simulation_data
!!
!! SYNOPSIS
!!  Use Simulation_data
!!
!! DESCRIPTION
!!
!!  Store the simulation data
!!
!! 
!!***
module Simulation_data

  implicit none

#include "constants.h"

  !! *** Runtime Parameters *** !!  

  real,    save :: sim_rhoCham_l
  real,    save :: sim_rhoCham_r
  real,    save :: sim_tempCham_l
  real,    save :: sim_tempCham_r

  real,    save :: sim_velxCham_l
  real,    save :: sim_velxCham_r

  integer, save :: sim_eosCham  

  real,    save :: sim_rhoMin
  real,    save :: sim_rhoMax
  real,    save :: sim_x0

  real, save :: sim_smallX
  character(len=MAX_STRING_LENGTH), save :: sim_initGeom


end module Simulation_data


