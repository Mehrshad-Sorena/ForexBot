from configparser import RawConfigParser


def globalConfig(filename='config.ini', section='global'):
    parser = RawConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]

    else:
        raise Exception('Section {0} not found in the {1} file'.format(
            section, filename))

    return db


def accountConfig(filename='config.ini', section='accounts'):
    parser = RawConfigParser()
    parser.read(filename)

    accounts = []
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]

    else:
        raise Exception('Section {0} not found in the {1} file'.format(
            section, filename))

    users = db.get('user').split(',')
    password = db.get('pass').split(',')
    types = db.get('type').split(',')
    for u, p, t in zip(users, password, types):
        accounts.append(
                {
                    'username': u,
                    'password': p,
                    'type': t
                }
        )
    return accounts


def mongoConfig(filename='config.ini', section='mongodb'):
    parser = RawConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]

    else:
        raise Exception('Section {0} not found in the {1} file'.format(
            section, filename))

    return db
