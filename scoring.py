import config as conf


def base_points(championship_standing, race_result):
    if (race_result == ''):
        return ''
    if (race_result == 'DNF'):
        return 50

    base_points = abs(race_result - championship_standing) + 10
    if (race_result == 3):
        base_points += 5
    if (race_result == 2):
        base_points += 5
    if (race_result == 1):
        base_points += 10

    return base_points


def multiplicator(race_guess, race_result):
    if (race_result == 'DNF' and race_guess == 'DNF'):
        return 1.0

    if (race_result == 'DNF' and race_guess != 'DNF'):
        return 0.0

    if (race_result != 'DNF' and race_guess == 'DNF'):
        return 0.0

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


def compute_scores(driver2stat):
    # Calculate per race points points
    for driver in conf.drivers:
        for race in conf.races:
            standing = driver2stat[driver][race]['champoinship standing']
            result = driver2stat[driver][race]['race result']

            patrick_tip = driver2stat[driver][race]['Patrick tip']
            lukas_tip = driver2stat[driver][race]['Lukas tip']
            lisa_tip = driver2stat[driver][race]['Lisa tip']

            driver2stat[driver][race]['base_points'] = base_points(standing, result)

            driver2stat[driver][race]['Lukas multiplicator'] = multiplicator(lukas_tip, result)
            driver2stat[driver][race]['Patrick multiplicator'] = multiplicator(patrick_tip, result)
            driver2stat[driver][race]['Lisa multiplicator'] = multiplicator(lisa_tip, result)

            driver2stat[driver][race]['Patrick points'] = points(standing, result, patrick_tip)
            driver2stat[driver][race]['Lukas points'] = points(standing, result, lukas_tip)
            driver2stat[driver][race]['Lisa points'] = points(standing, result, lisa_tip)
