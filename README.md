# poloscripts
1. Install - https://git-scm.com/
2. Installl poetry - https://python-poetry.org/docs/
3. Clone repo - git clone https://github.com/jcPOLO/poloscripts.git

Nornir3
1. Setup python virtual env with poetry. poetry shell.
2. Install dependencies with poetry. poetry install.
3. Add to your path this var. Ubuntu, you can add this to your .bashrc file.
export NET_TEXTFSM=$HOME/poloscripts/nornir-scripts/ntc-templates/templates/

Poloscripts
1. Setup python virtual environment. python3 -m venv venv.
2. Activate virtual env. source venv/bin/activate
3. Upgrade python pip. pip install --upgrade pip
4. Install dependencies. pip install -r requierements.txt

Inventory maker
1. cd ping_net/
2. python ping_net.py -n {net/mask}
3. cp {net_mask}.txt ../snmp_query/.
4. cd ../snmp_query/
5. python inventory_maker.py -f {net_mask}.txt

Output to csv/excel, we can open it and fill new ip address to be configured, remove duplicates, filter by column... 
model column is not supported by nornir3 script at the moment (neither bootstraping or filtering), so better remove it from csv.

----
Nornir3 Usage
1. cd nornir3/
2. python main.py
