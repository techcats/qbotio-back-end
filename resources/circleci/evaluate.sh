rm -rf ./qbotio-resources
git clone https://github.com/techcats/qbotio-resources.git ./qbotio-resources
cd ./qbotio-resources/
pip install -r requirements.txt
bash ./eval_suite.sh
cd ..
