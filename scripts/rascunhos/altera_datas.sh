#!/bin/bash

yesterday=`date -d "yesterday" +%Y%m%d`
two_days_ago=`date -d "-2 day" +%Y%m%d`
final_1=`date -d "+3 day" +%Y%m%d` 
final_2=`date -d "+4 day" +%Y%m%d`

echo yesterday
echo two_days_ago
echo final_1
echo final_2

sed -i "s/$two_days_ago/$yesterday/" /home/piatam8/ww3/ww3_shell/modelo_operacional/work/ww3_multi.inp.umdia

sed -i "s/$final_1/$final_2/" /home/piatam8/ww3/ww3_shell/modelo_operacional/work/ww3_multi.inp.umdia

sed -i "s/$two_days_ago/$yesterday/" /home/piatam8/ww3/ww3_shell/modelo_operacional/resultados/ww3_ounf.inp

sed -i "s/$two_days_ago/$yesterday/" /home/piatam8/ww3/ww3_shell/modelo_operacional/resultados/ww3_ounp.inp
