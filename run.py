from src.config import globalConfig, accountConfig
from src import ForexRobot

gconfig = globalConfig()
accounts = accountConfig()
act = accounts[0]

# create forex robot object
forex = ForexRobot()
# forex login
forex.login(act)

result = forex.run()
