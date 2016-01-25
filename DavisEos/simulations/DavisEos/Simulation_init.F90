!!****if* source/Simulation/SimulationMain/LaserSlab/Simulation_init
!!
!! NAME
!!
!!  Simulation_init
!!
!!
!! SYNOPSIS
!!
!!  Simulation_init()
!!
!!
!! DESCRIPTION
!!
!!  Initializes all the parameters needed for a particular simulation
!!
!!
!! ARGUMENTS
!!
!!  
!!
!! PARAMETERS
!!
!!***

subroutine Simulation_init()
  use Simulation_data
  use RuntimeParameters_interface, ONLY : RuntimeParameters_get
  use Logfile_interface, ONLY : Logfile_stamp
  
  implicit none

#include "constants.h"
#include "Flash.h"

  real :: xmin, xmax, ymin, ymax
  integer :: lrefine_max, nblockx, nblocky
  character(len=MAX_STRING_LENGTH) :: str


  call RuntimeParameters_get('sim_rhoCham_l', sim_rhoCham_l)
  call RuntimeParameters_get('sim_rhoCham_r', sim_rhoCham_r)
  call RuntimeParameters_get('sim_tempCham_l', sim_tempCham_l)
  call RuntimeParameters_get('sim_tempCham_r', sim_tempCham_r)

  call RuntimeParameters_get('sim_rhoMin', sim_rhoMin)
  call RuntimeParameters_get('sim_rhoMax', sim_rhoMax)

  call RuntimeParameters_get('smallX', sim_smallX)

end subroutine Simulation_init
