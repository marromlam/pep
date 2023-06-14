##source /afs/cern.ch/sw/lcg/external/gcc/5.2.0/x86_64-slc6/setup.sh
source /cvmfs/sft.cern.ch/lcg/external/gcc/6.2/x86_64-slc6/setup.sh
#source /cvmfs/sft.cern.ch/lcg/releases/gcc/6.2.0/x86_64-slc6/setup.sh

#source /afs/cern.ch/sw/IntelSoftware/linux/17-all-setup.sh < yeah
#source /cvmfs/projects.cern.ch/intelsw/psxe/linux/17-all-setup.sh
#source /cvmfs/projects.cern.ch/intelsw/psxe/linux/all-setup.sh intel64
source /cvmfs/projects.cern.ch/intelsw/psxe/linux/18-all-setup.sh intel64

#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/afs/cern.ch/sw/IntelSoftware/linux/x86_64/xe2017/compilers_and_libraries_2017.0.098/linux/tbb/lib/intel64_lin/gcc4.7/
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2017/compilers_and_libraries_2017.7.259/linux/tbb/lib/intel64/gcc4.7/

#source /var/opt/comp/source-comp.sh gcc 6.2.0
#source /var/opt/comp/source-comp.sh icc 2018

export PATH=/var/opt/sde-8.59/:$PATH
export LD_LIBRARY_PATH=/var/opt/sde-8.59/intel64/:$LD_LIBRARY_PATH

export PATH=/var/opt/PEP:$PATH

echo "-----------------------------------------------------------"
echo "Tool versions set up (expecting GCC 6.2 and Intel 2018)"
gcc --version
g++ --version
icc --version
icpc --version
sde64 --version
perf --version

echo "-----------------------------------------------------------"
MODEL=`cat /proc/cpuinfo  | grep model | head -1 | cut -f2 -d:`
if [ "$MODEL" = " 63" ]
then
	echo "You are on a HASWELL system"
elif [ "$MODEL" = " 62" ]
then
	echo "You are on an IVY BRIDGE system"
else
	echo "Unknown architecture - please ask the speaker"
fi
