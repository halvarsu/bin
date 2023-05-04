#!

CURR_TIME=$(date -Iminutes)

echo "saving current jobs to ~/jobs/$CURR_TIME"
print_workdirs.sh > ~/jobs/$CURR_TIME
echo "done"
