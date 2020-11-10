#!/bin/bash
#: Trying if .... else ....
#: VAP

guess=$RANDOM
check=1111
count=0
while [ $check -eq 1111 ]
do
count=$(( $count + 1 ))
printf "\n ========= GUESS MY NUMBER ========== \n Enter your Guess$  "
read number

#: /dev/null is a bitbucket

if [ -z "$number" ] #: This is for checking the input value in test [ .. ]
then
	printf 'None Entered \n' >&2
	#exit 1 ## Set a failed return code
fi

if [ "$number" -gt "$guess" ]
then 
	printf "The number is too high --> %d\n" "$number" >& 2
elif [ "$number" -lt $guess ]
then 
	printf "The number is too low --> %d\n" "$number" >& 2
elif [ "$number" -eq "$guess" ]
then
	printf "CONGRATZZZ ... You have won the game \n"
	printf "Your have finished in %d try ...\n" "$count"
	exit 0
else
	printf " OOPs!! Wrong INPUT.. Try Again ...\n" 
fi
done

# i=2; for ((;;)); do printf "$i\n"; i=$(( i + 1 )); done | ./if 
