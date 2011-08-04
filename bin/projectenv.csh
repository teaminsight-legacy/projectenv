#!/bin/csh

if ($?return_to) unset return_to

if ($?PROJECTENV_PATH) then
else
  setenv PROJECTENV_PATH `python -m projectenv.__main__ path`
endif

if ($1 == 'sync') then
  goto __projectenv__pre_sync # I know, I know, but... csh does not have functions!
else if ($1 == 'on') then
  goto __projectenv__pre_on
else if ($1 == 'off') then
  goto __projectenv__off
else if ($#argv > 0) then
  goto __projectenv__python
endif

##
# skip pseudo-functions
##
goto done

__projectenv__pre_sync:
  set return_to = __projectenv__sync
  goto __projectenv__off

__projectenv__sync:
  set return_to = __projectenv__post_sync
  goto __projectenv__python

__projectenv__post_sync:
  if ($__last_exit_status == 0) then
    goto __projectenv__on
  endif
  goto done

__projectenv__pre_on:
  set return_to = __projectenv__on
  goto __projectenv__off

__projectenv__on:
  set env_name = `pwd | grep -o -E '[^/]+$'`
  source "$PROJECTENV_HOME/environments/$env_name/bin/activate.csh"
  source $VIRTUAL_ENV/bin/post_activate.csh
  goto done

__projectenv__off:
  if ($?VIRTUAL_ENV) then
    set pre_deactivate = "$VIRTUAL_ENV/bin/pre_deactivate.csh"
    if (-e $pre_deactivate) then
      source $pre_deactivate
    endif
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
  set __last_exit_status = $?

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
