#!/bin/csh

if ($?return_to) unset return_to

if ($?PROJECTENV_PATH) then
else
  setenv PROJECTENV_PATH `python -m projectenv.__main__ path`
endif

if ($1 == 'sync') then
  goto __projectenv__sync # I know, I know, but... csh does not have functions!
else if ($1 == 'on') then
  goto __projectenv__on
else if ($1 == 'off') then
  goto __projectenv__off
else if ($#argv > 0) then
  goto __projectenv__python
endif

##
# skip pseudo-functions
##
goto done

__projectenv__sync:
  set env_name = `pwd | grep -o -E '[^/]+$'`
  source $PROJECTENV_HOME/environments/$env_name/bin/activate.csh
  set return_to = __projectenv__post_sync
  goto __projectenv__python

__projectenv__post_sync:
  if ($? == 0) then
    deactivate
    goto __projectenv__on
  else
    deactivate
  endif
  goto done

__projectenv__on:
  if ($?VIRTUAL_ENV) then
    set return_to = __projectenv__on
    goto __projectenv__off
  endif

  set env_name = `pwd | grep -o -E '[^/]+$'`
  source "$PROJECTENV_HOME/environments/$env_name/bin/activate.csh"
  source $VIRTUAL_ENV/bin/post_activate.csh
  goto done

__projectenv__off:
  if ($?VIRTUAL_ENV) then
    source $VIRTUAL_ENV/bin/pre_deactivate.csh
    deactivate
  endif

  if ($?return_to) then
    goto $return_to
  endif
  goto done

__projectenv__python:
  if ($?PYTHONPATH) then
    setenv PROJECTENV_OLD_PYTHONPATH $PYTHONPATH
    setenv PYTHONPATH ${PROJECTENV_PATH}:${PYTHONPATH}
  else
    setenv PYTHONPATH $PROJECTENV_PATH
  endif

  python $PROJECTENV_PATH $*

  if ($?PROJECTENV_OLD_PYTHONPATH) then
    setenv PYTHONPATH $PROJECTENV_OLD_PYTHONPATH
    unsetenv PROJECTENV_OLD_PYTHONPATH
  endif

  if ($?return_to) then
    goto $return_to
  endif
  goto done

# Leave this as the last line or you will break the script!!!
done:
