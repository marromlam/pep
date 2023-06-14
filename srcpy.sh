OPTVER=opt

## Python 2.7.9
#PYVER=2.7.9.p1-df007
#GCCVER=gcc48

## Python 3.5.2
PYVER=3.5.2-a1f64
GCCVER=gcc62

export PYTHONDIR="/cvmfs/sft.cern.ch/lcg/releases/Python/$PYVER/x86_64-slc6-$GCCVER-$OPTVER"
export LD_LIBRARY_PATH=$PYTHONDIR/lib:$LD_LIBRARY_PATH
export PATH=$PYTHONDIR/bin:$PATH
