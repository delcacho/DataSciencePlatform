./createcluster.sh
./validatecluster.sh
./createservices.sh
./waitpods.sh 1800 10
#rm -rf kflw
#./createkubeflow.sh
