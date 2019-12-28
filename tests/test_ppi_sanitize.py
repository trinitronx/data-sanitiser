from sanitize import sanitize

def test_ukphone():
    assert sanitize.replacePPI('test 02071831573') == 'test UKPHONE'
    assert sanitize.replacePPI('test 0207 183 1573') == 'test UKPHONE'
    assert sanitize.replacePPI('test 07837182113') == 'test UKPHONE'
    assert sanitize.replacePPI(' 07837182113 test') == ' UKPHONE test'

def test_email():
    assert sanitize.replacePPI(' aaaaaaa@bbbbb.com test') == ' NAME@EMAIL.COM test'
    assert sanitize.replacePPI(' a@b.com test') == ' NAME@EMAIL.COM test'
    assert sanitize.replacePPI(' a@b.io test') == ' NAME@EMAIL.COM test'
    assert sanitize.replacePPI(' 123@10.10.10.10 test') == ' NAME@EMAIL.COM test'
    assert sanitize.replacePPI('1a@2.com test') == 'NAME@EMAIL.COM test'
    assert sanitize.replacePPI(' test 1a@2.com test') == ' test NAME@EMAIL.COM test'
    assert sanitize.replacePPI('1a@2.com test') == 'NAME@EMAIL.COM test'
    assert sanitize.replacePPI('test 1a@2.com test 1a@2.com test') == 'test NAME@EMAIL.COM test NAME@EMAIL.COM test'

# http://rion.io/2013/09/10/validating-social-security-numbers-through-regular-expressions-2/
def test_ssn():
    assert sanitize.replacePPI('test 123-12-1234') == 'test SSN'
    assert sanitize.replacePPI('test 123 12 1234') != 'test SSN'
    assert sanitize.replacePPI('test 666-12-1234') != 'test SSN'
    assert sanitize.replacePPI('test 123-12-0000') != 'test SSN'
    assert sanitize.replacePPI('test 123-00-1234') != 'test SSN'
    assert sanitize.replacePPI('test 000-12-1234') != 'test SSN'
    assert sanitize.replacePPI('test 900-00-1234') != 'test SSN'
    assert sanitize.replacePPI('test 078-05-1120') != 'test SSN'
    assert sanitize.replacePPI('test 219-09-9999') != 'test SSN'

def test_canada_postcode():
    assert sanitize.replacePPI('test V9A 7N2') == 'test POSTCODECA'

def test_us_zipcode():
    assert sanitize.replacePPI('test 77801') == 'test ZIPCODEUS'

def test_cardnum():
    # Consumer Amex
    assert sanitize.replacePPI('test 371449635398431') == 'test CARDNUM'
    # Commercial Amex
    assert sanitize.replacePPI('test 378734493671000') == 'test CARDNUM'
    # Australian Bankcard
    #assert sanitize.replacePPI('test 5610591081018250') == 'test CARDNUM'
    # VISA:
    assert sanitize.replacePPI('test 4189514333444318') == 'test CARDNUM'
    assert sanitize.replacePPI('test 4532904128495944') == 'test CARDNUM'
    #assert sanitize.replacePPI('test 4556235228575679957') == 'test CARDNUM'
    # Discover:
    assert sanitize.replacePPI('test 6011140394576324') == 'test CARDNUM'
    assert sanitize.replacePPI('test 6011947899660985') == 'test CARDNUM'
    #assert sanitize.replacePPI('test 6011110646001136629') == 'test CARDNUM'
    # Diners Club - Carte Blanche:
    assert sanitize.replacePPI('test 30563039743969') == 'test CARDNUM'
    assert sanitize.replacePPI('test 30397311754059') == 'test CARDNUM'
    assert sanitize.replacePPI('test 30390414367101') == 'test CARDNUM'

    # Visa Electron:
    #assert sanitize.replacePPI('test 4913285379677151') == 'test CARDNUM'
    assert sanitize.replacePPI('test 4508300385930014') == 'test CARDNUM'
    assert sanitize.replacePPI('test 4917576565198556') == 'test CARDNUM'
    # MasterCard:
    assert sanitize.replacePPI('test 5362094316989957') == 'test CARDNUM'
    assert sanitize.replacePPI('test 2720992245099208') == 'test CARDNUM'
    assert sanitize.replacePPI('test 2221000131482316') == 'test CARDNUM'
    # JCB:
    assert sanitize.replacePPI('test 3539740511407301') == 'test CARDNUM'
    assert sanitize.replacePPI('test 3540232027278464') == 'test CARDNUM'
    assert sanitize.replacePPI('test 3537622269740481004') == 'test CARDNUM'
    # Diners Club - International:
    assert sanitize.replacePPI('test 36076547569788') == 'test CARDNUM'
    assert sanitize.replacePPI('test 36615981798112') == 'test CARDNUM'
    assert sanitize.replacePPI('test 36540004508860') == 'test CARDNUM'
    # InstaPayment:
    assert sanitize.replacePPI('test 6377564681522097') == 'test CARDNUM'
    assert sanitize.replacePPI('test 6392565607142788') == 'test CARDNUM'
    assert sanitize.replacePPI('test 6394009429937768') == 'test CARDNUM'
    # American Express (AMEX):
    assert sanitize.replacePPI('test 342618466580053') == 'test CARDNUM'
    assert sanitize.replacePPI('test 348306096076338') == 'test CARDNUM'
    assert sanitize.replacePPI('test 370788278587177') == 'test CARDNUM'
    # Diners Club - North America:
    assert sanitize.replacePPI('test 5513754137519741') == 'test CARDNUM'
    assert sanitize.replacePPI('test 5469096128695682') == 'test CARDNUM'
    assert sanitize.replacePPI('test 5542777111734585') == 'test CARDNUM'
    # Maestro:
    assert sanitize.replacePPI('test 5893403432036155') == 'test CARDNUM'
    assert sanitize.replacePPI('test 5018161721191285') == 'test CARDNUM'
    assert sanitize.replacePPI('test 5893341704932828') == 'test CARDNUM'
