for i in $(seq 1 1000)
do	
	echo $i > ejecucion
	echo $($1)
done
