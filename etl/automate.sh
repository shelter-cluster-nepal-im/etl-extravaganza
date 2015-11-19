#automate weekly database update procedures

ssh -tt -i ~/.ssh/shelter-cluster.pem $1 \
"source ~/.bash_profile;
cd /home/ec2-user/etl-extravaganza/;
sudo git stash; git pull;
sudo python setup.py install;
echo \"pulled\";
cd etl/sql/;
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
