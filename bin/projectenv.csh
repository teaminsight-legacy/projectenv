#!/bin/csh

if ($?return_to) unset return_to

if ($1 == 'sync') then
  goto __projectenv__sync # I know, I know, but... csh does not have functions!
else if ($1 == 'on') then
  goto __projectenv__on
else if ($1 == 'off') then
  goto __projectenv__off
else if ($#argv > 0) then
  goto __projectenv
endif

##
# skip pseudo-functions
##
goto hell

__projectenv:
  python $PROJECTENV_HOME/bin/projectenv.py $*
  goto hell

__projectenv__sync:
  set env_name = `pwd | grep -o -E '[^/]+$'`
  source $PROJECTENV_HOME/environments/$env_name/bin/activate.csh
  python $PROJECTENV_HOME/bin/projectenv.py $*
  if ($? == 0) then
    deactivate
    goto __projectenv__on
  else
    deactivate
  endif
  goto hell

__projectenv__on:
  if ($?VIRTUAL_ENV) then
    set return_to = __projectenv__on
    goto __projectenv__off
  endif
  set env_name = `pwd | grep -o -E '[^/]+$'`
  source "$PROJECTENV_HOME/environments/$env_name/bin/activate.csh"
  source $VIRTUAL_ENV/bin/post_activate.csh
  goto hell

__projectenv__off:
  if ($?VIRTUAL_ENV) then
    source $VIRTUAL_ENV/bin/pre_deactivate.csh
    deactivate
  endif
  if ($?return_to) then
    goto $return_to
  endif
  goto hell

# Leave this as the last line or you will break the script!!!
hell:
