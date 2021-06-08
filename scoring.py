import config as conf


def base_points(championship_standing, race_result):
    if (race_result == '' or championship_standing == ''):
        return ''
    if (race_result == 'DNF'):
        return 50

    race_result = int(float(race_result))
    championship_standing = int(float(championship_standing))
    base_points = abs(race_result - championship_standing) + 10
    if (race_result == 3):
        base_points += 5
    if (race_result == 2):
        base_points += 5
    if (race_result == 1):
        base_points += 10

    return base_points


def multiplicator(race_guess, race_result):
    if race_guess == '' or race_result == '':
        return ''

    if (race_result == 'DNF' and race_guess == 'DNF'):
        return 1.0

    if (race_result == 'DNF' and race_guess != 'DNF'):
        return 0.0

    if (race_result != 'DNF' and race_guess == 'DNF'):
        return 0.0

    race_result = int(float(race_result))  # TODO(scheuclu) Remove construct
    race_guess = int(float(race_guess))
    diff = abs(race_result - race_guess);
    if (diff == 0):
        return 3.0
    if (diff == 1):
        return 2.0
    if (diff == 2):
        return 1.0

    return 0.0


def points(championship_standing, race_result, race_guess):
    return base_points(championship_standing, race_result) * multiplicator(race_guess, race_result)


def score_race(df):
    # First, clear out the existing rows
    df.loc['base points'] = ''
    for player in ['Lukas', 'Patrick', 'Lisa']:
        df.loc[f'{player} points'] = ''
        df.loc[f'{player} multiplicator'] = ''

    for driver in conf.drivers:
        race_result = df[driver]['race result']
        champoinship_standing = df[driver]['champoinship standing']
        if race_result == '' or champoinship_standing == '':
            continue
        bp = base_points(champoinship_standing, race_result)
        df[driver]['base points'] = str(bp)
        for player in ['Lukas', 'Lisa', 'Patrick']:
            tip = df[driver][f'{player} tip']
            if tip == '':
                continue
            mult = multiplicator(tip, race_result)
            df[driver][f'{player} multiplicator'] = str(int(mult))
            df[driver][f'{player} points'] = str(int(bp * mult))


def compute_scores2(races2data):
    for df in races2data.values():
        score_race(df)


def compute_scores(driver2stat):
    # Calculate per race points points
    for driver in conf.drivers:
        for race in conf.races:
            standing = driver2stat[driver][race]['champoinship standing']
            result = driver2stat[driver][race]['race result']
            if standing == '' or result == '':
                continue

            driver2stat[driver][race]['base points'] = base_points(standing, result)

            lukas_tip = driver2stat[driver][race]['Lukas tip']
            if lukas_tip != '':
                driver2stat[driver][race]['Lukas multiplicator'] = multiplicator(lukas_tip, result)
                driver2stat[driver][race]['Lukas points'] = points(standing, result, lukas_tip)

            patrick_tip = driver2stat[driver][race]['Lukas tip']
            if patrick_tip != '':
                driver2stat[driver][race]['Patrick multiplicator'] = multiplicator(patrick_tip, result)
                driver2stat[driver][race]['Patrick points'] = points(standing, result, patrick_tip)

            lisa_tip = driver2stat[driver][race]['Lisa tip']
            if lisa_tip != '':
                driver2stat[driver][race]['Lisa multiplicator'] = multiplicator(lisa_tip, result)
                driver2stat[driver][race]['Lisa points'] = points(standing, result, lisa_tip)
