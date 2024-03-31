#final project
#!/bin/bash

start=1
while [ "$start" -eq 1 ]

do



echo "choose an option
1) Generate mannual 
2) Search for command manuual
3) Verification
4) Recommandition
5) exit"

read option

#-------------------------------------------------------
if [ "$option" -eq 1 -o "$option" -eq 3 ] 
then
genetare_verif_mannual(){

echo "" > allcommands.txt # to remove previous content

for command in   lspci cd ls grep printf mkdir ss paste uniq  cp tr alias rmdir test wc date uname vmstat ps sed who pipe man pwd chmod
do
#*****************************************************************
# Get command description

description=$(man $command | awk '/^DESCRIPTION/,/^OPTIONS/' | grep -v '^OPTIONS'| head -5 )


#*****************************************************************
# Get command version
version=$($command --version 2> /dev/null | head -2) 
if [ -z "$version" ]
then 
version=$(man $command | awk '/^VERSIONS/,/^NOTES/' | grep -v '^NOTES')
fi
if [ -z "$version" ]
then 
version=$(uname -r)
fi

#******************************************************************

# Get example
example=""
 case $command in
        "cd")
            example="$command ~ # Change to  home directory "  
            ;;
        "grep")
            example=" $command  'pattern'  file_name" 
            ;;
        "printf")
            example=" $command  '%s' 'Hello World!'"
            ;;
        "mkdir")
            example="$command new_directory_name"
            ;;

        "paste")
            example=" $command  -s  filename "
            ;;
        "uniq")
            example=" $command sorted_file " 
            ;;
        "cp")
            example="$command file.txt copied_file.txt"
            ;;
        "tr")#
            example=" $command oldpattern newpattern < filename "
            ;;
        "alias")
            example="$command ls='ls -aF'"
            ;;
        "rmdir")
            example="mkdir n_directory; $command n_directory"
            ;;
        "test")
            example="$command -e file.txt ; echo $? # test file if exisit" 
            ;;
        "chmod")
            example=" $command +x script.sh"
            ;;
         "man")
            example=" $command command_name 
            man man "
            ;;
        "wc")#
            example="$command filename "
            ;;
        "sed")
            example=" $command 's/old/new/' filename "
            ;;
            
       "pipe") 
         example=" sort allcommands.txt | cat  " ;;  
         
        *)
        
        if [ "$command" != "lspci" ] 
        then
       example=$("$command" | head -10)
       fi
 	if [ -z "$example" ]
	then 
          # Default example (just the command itself)
 	example=" "$command" -t :
	$("$command" -t 2> /dev/null  | head -10) "
            fi
            
   ;;
   
   
   
    esac
	
#******************************************************************

# Get related commands
if [ $command = lspci -o  $command = mkdir -o $command = rmdir -o $command = chmod  ]
then
related_commands=$(compgen -A function -abck | grep  "${command: -3}"| grep -v $command | head -15)

elif [ $command = printf -o $command = uniq ]
then
related_commands=$(compgen -A function -abck | grep  "${command:0:3}" | grep -v $command |  head -15)
elif [ $command = uname -o $command = vmstat ]
then
related_commands=$(compgen -A function -abck | grep "${command: -4}"| grep -v $command | head -15) 

else
related_commands=$(compgen -A function -abck | grep -o '[^[:space:]]*'$command'[^[:space:]]*' | grep -v '^'$command'$' | head -15)

fi


unique_commands=$(echo $related_commands | tr ' ' '\n' | sort -u)
#*******************************************************************

manual=$(printf "\n \033[1m%s:\033[0m
___________________________________________________________________________ \033[1m\033[1m\n\033[4mDESCRIPTION:\n\033[0m\033[3m%s\033[0m\n
___________________________________________________________________________ \033[1m\033[1m\n\033[4m VERSION:\n\033[0m \033[3m      %s\033[0m\n
___________________________________________________________________________ \033[1m\033[1m\n\033[4m EXAMPLE OF %s :\n\033[0m \n\033[3m       %s\033[0m\n
___________________________________________________________________________ \033[1m\033[1m\n\033[4mRELATED COMMAND:\n\033[0m\033[3m%s\033[0m\n
___________________________________________________________________________
" "$command" "$description" "$version" "$command" "$example" "$unique_commands")

echo $command >> allcommands.txt

	if [ "$option" -eq 1 ]
	then
# Append manual entry to document file
	printf "%s\n\n" "$manual" > "$command".txt

	else
# Append manual entry to document file
	printf "%s\n\n" "$manual" >  "${command}_Ver".txt

	fi
done
}




fi



#------------------------------------------------------------------------

 case "$option"
in 
1)
echo "Wait>>>"
genetare_verif_mannual

printf "_________________________________________________________
\nManual entry for the following commands have been created\n"
#printf " enter cat command.txt to see the manual \n "
 sort allcommands.txt | cat 

;;

#*******************************************************
2)   


echo "choose the command name you want to see its manuual"
 cat allcommands.txt | sort 
 

	read command
	while ! grep -q "$command" allcommands.txt;do
	echo "$command not found.Please re-enter commad name"
	read command
	done
	
cat "$command".txt

	recomm command 
     	getrelatedcommand 
     	printf "%s\n" "$unique_commands" 

echo ""
;;


#*****************************************************
3)
echo "verification>>> Wait..." 


genetare_verif_mannual 

echo "
enter 
1) if you want to verfiy all commands mannual
2) if you want to verify specific command
"
read veropt
case "$veropt"
in
1)
for comm in   lspci cd ls grep printf mkdir ss paste uniq  cp tr alias rmdir test wc date uname vmstat ps sed who pipe man pwd chmod
do
verfiy comm # verfication function
done
;;
#%%%%%%%%
2)
echo "choose the command name you want to verify its manuual "
sort allcommands.txt | tr '\n' ' ' |cat
printf "\n"
read comm

while [ "$comm" != "q" ]
do

	while ! grep -q "$comm" allcommands.txt;do
	echo "$comm not found.Please re-enter commad name"
	read comm
	done


  verfiy comm # verfication function


echo "
TYPE (q) IF YOU DONE OR IF YOU WANT TO VERIFY ANOTHER COMMAND 
TYPE THE COMMAND NAME "
read comm
done
;;

*) echo "enter valid oprion" ;;
esac
;;
#**************************************************************
4)

echo "Enter command name !"
read command 

	while ! grep -q "$command" allcommands.txt;do
	echo "$command not found.Please re-enter commad name"
	read command
	done

 	recomm command  
	getrelatedcommand

printf "%s\n" "$unique_commands"

echo ""
;;
5) exit  ;;

*) echo "enter a valid option"
esac

#$$$$$$$$$$$$$$$$$$$$$$$$$
function verfiy(){
local parameter=$1

 if [ "$comm" != "ls" -a  "$comm" != "ss" -a  "$comm" != "date" -a "$comm" != "ps" -a  "$comm" != "vmstat" -a  "$comm" != "pwd" -a "$comm" != "man" -a "$comm" != "tr" ]
then

result=$(cmp -s "${comm}_Ver".txt "$comm".txt)

elif [ "$comm" != man -a "$comm" != "tr" ]
then
 # Read the contents of command.txt and remove lines between "example" and "related command" > bcz for these command the timing differ
 
sed '/EXAMPLE OF/,/RELATED COMMAND/d' "$comm".txt > file1_modified.txt

# Read the contents of file11.txt and remove lines between "example" and "related command"
sed '/EXAMPLE OF/,/RELATED COMMAND/d' "${comm}_Ver".txt > file11_modified.txt

# Compare the modified contents of the two files
res=$(cmp -s file1_modified.txt file11_modified.txt)
else

sed '/RELATED/,/______/d' "$comm".txt > file1_modified.txt

# Read the contents of file11.txt and remove lines between "example" and "related command"
sed '/RELATED/,/_____/d' "${comm}_Ver".txt > file11_modified.txt

# Compare the modified contents of the two files
res=$(cmp -s file1_modified.txt file11_modified.txt)


fi


    if [ $? -eq 0 ]
    then
        echo "verfication done for "$comm" command manuual is up to date"
    else
        echo " "$comm" not complete regenerate mannulas "
    fi
    



}
#$$$$$$$$$$$$$$$$$$$$$$$$$
function getrelatedcommand(){

# Get related commands
if [ $command = lspci -o  $command = mkdir -o $command = rmdir -o $command = chmod  ]
then
related_commands=$(compgen -A function -abck | grep  "${command: -3}"| grep -v $command | head -7)

elif [ $command = printf -o $command = uniq ]
then
related_commands=$(compgen -A function -abck | grep  "${command:0:3}" | grep -v $command |  head -7)
elif [ $command = uname -o $command = vmstat ]
then
related_commands=$(compgen -A function -abck | grep "${command: -4}"| grep -v $command | head -15) 

else
related_commands=$(compgen -A function -abck | grep -o '[^[:space:]]*'$command'[^[:space:]]*' | grep -v '^'$command'$' | head -7)

fi


unique_commands=$(echo $related_commands | tr ' ' '\n' | sort -u)
}

#%%%%%

function  recomm(){
printf " 
	\033[1m\033[1m\n\033[4mRecommended command:\n\033[0m"

local parameter=$1
case "$command" in 

    "grep") echo "find" ;;
    "cp") printf  "mv\ncat\n" ;;
    "uniq") printf "sort\ncat\n" ;;
    "paste")  printf "cut\nawk\n" ;;
    "ls")  printf "cd\ncat\n" ;;
    "printf") printf "echo\ncolumn\nsed\ncat\n" ;;
    "mkdir")  printf "cd\nls\nmvdir\nmdir\nrm\n" ;;
    "rmdir") printf "ls\nrm\nmkdir\nmdir\n" ;;
    "cd") echo "ls" ;;
    "alias") echo "unalias" ;;
    "tr") printf "sed\ncut\nawk\n" ;;
    "test") printf "if\n[]\n" ;;
    "chmod") printf "pico\n./\n" ;;
    "wc") printf "cat\ngrep\nsed\ntr\ncat\n" ;;
    "sed") printf "tr\nprintf\nawk\ncat\n" ;;
    "who") printf "chmod\n" ;;
    "pipe") printf "awk\nsed\nsort\nuniq\ncat\n" ;;
    "man") printf "grep\n" ;;
 

 *) echo "" ;;
 
  esac
}


done


