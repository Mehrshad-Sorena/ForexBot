from configparser import RawConfigParser

def accountConfig(filename='Mt5_config.ini', section='accounts'):
    parser = RawConfigParser()
    parser.read(filename)

    accounts = dict()
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]

    else:
        raise Exception('Section {0} not found in the {1} file'.format(
            section, filename))

    name = db.get('name').split(',')
    users = db.get('username').split(',')
    password = db.get('password').split(',')
    types = db.get('type').split(',')
    for n, u, p, t in zip(name, users, password, types):
        accounts.update(
                {
                    n: {
                        'username': u,
                        'password': p,
                        'type': t
                    }
                }
        )
    return accounts
