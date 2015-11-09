#automate weekly database update procedures

ssh -tt -i ~/.ssh/shelter-cluster.pem $1 \
"source ~/.bash_profile;
cd /home/ec2-user/etl-extravaganza/etl;
sudo git pull;
echo \"pulled\";
python master_db_creation.py --path '$2' --location db --table_name distributions;
echo \"distributions completed\";
python master_dbTrain_creation.py --path '$2' --location db --table_name training;
echo \"training completed\";" > /tmp/out.txt 2>&1

ssh -tt -i ~/.ssh/shelter-cluster.pem $3 \
"source ~/.bash_profile;
cd /home/ec2-user/thetablesarepivoting/scripts/;
sudo git pull;
echo \"pulled\";
sudo python make_districts.py;
echo \"consider them made\";" >> /tmp/out.txt 2>&1

cat /tmp/out.txt

ssh -i ~/.ssh/shelter-cluster.pem ec2-user@ec2-52-3-170-125.compute-1.amazonaws.com
python /home/ec2-user/etl-extravaganza/etl/master_db_creation.py --path \"2015 Nepal EQ/04 IM/Reporting/Reporting/Database_&_Template/DatabaseV5.0_30_10_2015.xlsx\" --location db --table_name distributions;"
