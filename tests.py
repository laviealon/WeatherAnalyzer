import pytest
from datetime import date
from weather import DailyWeather, HistoricalWeather, Country, load_data


################################################################################
# Sample test cases below
#
# Use the test cases below as an example for writing your own test cases,
# and as a start to testing your A0 code. Most of these test functions create
# objects "by hand" that are used for testing methods.  Once you implement
# function load_data, you will be able to create an HistoricalWeather object
# by calling load_data, or a Country object by calling load_country. You may
# find this makes testing easier.
#
# The self-test on MarkUs runs the tests below, along with a few others.
# Make sure you run the self-test on MarkUs after submitting your code!
#
# You do not have to submit this file for A0. This is for your own use.
#
# WARNING: THIS IS CURRENTLY AN EXTREMELY INCOMPLETE SET OF TESTS!
# We will test your code on a much more thorough set of tests!
################################################################################
def test_add_and_retrieve_weather():
    """Test that we can add and retrieve a single weather record from
    HistoricalWeather."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))
    daily = DailyWeather((1, 2, 3), (4, 2, 2))
    record_date = date(2020, 1, 12)
    historical.add_weather(record_date, daily)

    assert historical.retrieve_weather(record_date) is daily, \
        "Calling retrieve_weather() on a date should return the " + \
        "DailyWeather object that was added to that date."


def test_record_high():
    """Test record_high on a HistoricalWeather with two points of data, where the
    record high is at the earlier year."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))

    historical.add_weather(date(2012, 6, 4),
                           DailyWeather((0, 0, 20), (0, 0, 0)))

    historical.add_weather(date(2010, 6, 4),
                           DailyWeather((0, 0, 30), (0, 0, 0)))

    assert historical.record_high(6, 4) == 30


def test_monthly_average():
    """Test monthly_average on a HistoricalWeather that has one point of data
    per month, all within a single year."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))

    historical.add_weather(date(2012, 1, 8),
                           DailyWeather((-0.25, -1.75, 0.25), (0, 0, 0)))

    historical.add_weather(date(2012, 2, 9),
                           DailyWeather((0.0, -3.0, 1.0), (0, 0, 0)))

    historical.add_weather(date(2012, 3, 10),
                           DailyWeather((0.75, -3.75, 2.25), (0, 0, 0)))

    historical.add_weather(date(2012, 4, 11),
                           DailyWeather((2.0, -4.0, 4.0), (0, 0, 0)))

    historical.add_weather(date(2012, 5, 12),
                           DailyWeather((3.75, -3.75, 6.25), (0, 0, 0)))

    historical.add_weather(date(2012, 6, 13),
                           DailyWeather((6.0, -3.0, 9.0), (0, 0, 0)))

    historical.add_weather(date(2012, 7, 14),
                           DailyWeather((8.75, -1.75, 12.25), (0, 0, 0)))

    historical.add_weather(date(2012, 8, 15),
                           DailyWeather((12.0, 0.0, 16.0), (0, 0, 0)))

    historical.add_weather(date(2012, 9, 16),
                           DailyWeather((15.75, 2.25, 20.25), (0, 0, 0)))

    historical.add_weather(date(2012, 10, 17),
                           DailyWeather((20.0, 5.0, 25.0), (0, 0, 0)))

    historical.add_weather(date(2012, 11, 18),
                           DailyWeather((24.75, 8.25, 30.25), (0, 0, 0)))

    historical.add_weather(date(2012, 12, 19),
                           DailyWeather((30.0, 12.0, 36.0), (0, 0, 0)))

    assert historical.monthly_average() == {'Jan': -1.75, 'Feb': -3.0,
                                            'Mar': -3.75, 'Apr': -4.0,
                                            'May': -3.75, 'Jun': -3.0,
                                            'Jul': -1.75, 'Aug': 0.0,
                                            'Sep': 2.25, 'Oct': 5.0,
                                            'Nov': 8.25, 'Dec': 12.0
                                            }


def test_contiguous_precipitation():
    """Test contiguous_precipitation on a HistoricalWeather that has alternating
    snow and rain."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))

    historical.add_weather(date(2012, 6, 4),
                           DailyWeather((0, 0, 0), (3, 3, 0)))

    historical.add_weather(date(2012, 6, 5),
                           DailyWeather((0, 0, 0), (2, 0, 2)))

    historical.add_weather(date(2012, 6, 6),
                           DailyWeather((0, 0, 0), (4, 4, 0)))

    historical.add_weather(date(2012, 6, 7),
                           DailyWeather((0, 0, 0), (1, 0, 1)))

    historical.add_weather(date(2012, 6, 8),
                           DailyWeather((0, 0, 0), (5, 5, 0)))

    assert historical.contiguous_precipitation() == (date(2012, 6, 4), 5)


def test_percentage_snowfall():
    """Test percentage_snowfall on a HistoricalWeather that has a single day
    with both snow and rain"""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))

    historical.add_weather(date(2012, 11, 21),
                           DailyWeather((0, 0, 0), (7, 3, 2)))

    assert historical.percentage_snowfall() == 0.4


def test_add_and_retrieve_history():
    """Test that we can add and retrieve a single weather record from
    a Country."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))
    country = Country("Country Name")
    country.add_history(historical)

    assert country.retrieve_history("City Name") is historical, \
        "Calling retrieve_history() on a location should return the " + \
        "HistoricalWeather object that was added to that location."


def test_snowiest_location():
    """Test that snowiest_location with two locations returns the one with a
    higher percentage snowfall."""
    country = Country('Country Name')

    # Create one HistoricalWeather record
    historical = HistoricalWeather('City Name', (-1.234, 4.567))

    historical.add_weather(date(2012, 11, 21),
                           DailyWeather((-5, -10, 15), (7, 3, 2)))

    historical.add_weather(date(2012, 10, 21),
                           DailyWeather((-7, -20, 15), (0, 0, 0)))

    historical.add_weather(date(2011, 11, 21),
                           DailyWeather((-8, -15, 15), (0, 0, 0)))

    country.add_history(historical)

    # Create another HistoricalWeather record
    historical2 = HistoricalWeather("Another City", (0.123, -3.4567))

    historical2.add_weather(date(2012, 11, 21),
                            DailyWeather((-5, -10, 15), (9, 5, 4)))

    historical2.add_weather(date(2012, 10, 21),
                            DailyWeather((-7, -20, 15), (20, 15, 5)))

    country.add_history(historical2)

    assert country.snowiest_location() == ('City Name', 0.4)


def test_load_data():
    """Test load_data on small_sample_data.csv"""
    with open('weather_data/small_sample_data.csv') as source:
        historical_weather = load_data(source)

    assert historical_weather is not None, \
        "HistoricalWeather should have been returned when calling load_data " \
        "on small_sample_data.csv but got None."

    assert historical_weather.name == 'THUNDER BAY'


def test_load_data_empty():
    """Test that load_data returns None on an empty csv file"""
    with open('weather_data/empty_sample_data.csv') as source:
        historical_weather = load_data(source)

    assert historical_weather is None


"""Tests for class DailyWeather"""


def test_daily_weather_init_and_str():
    dw = DailyWeather((10, 5, 20), (16, -1, 12))
    assert dw.avg_temp == 10
    assert dw.low_temp == 5
    assert dw.high_temp == 20
    assert dw.precipitation == 16
    assert dw.rainfall == -1
    assert dw.snowfall == 12
    assert dw.__str__() == 'Average: 10 Low: 5 High: 20 Precipitation: 16 Snow: 12 Rain: -1'


"""Tests for class HistoricalWeather"""

"""
def test_historical_weather_init_and_str():
    dw1 = DailyWeather((10, 5, 20), (16, -1, 12))
    dw2 = DailyWeather((5, -10, 15), (-1, -1, 5))
    dw3 = DailyWeather((6, -11, 17), (10, 3, 2))
    hw1 = HistoricalWeather('New York', (1, 2))
    hw2 = HistoricalWeather('Toronto', (3,1))
    hw1.add_weather(date.today(), dw1)
    hw1.add_weather(date(2018,12,1), dw2)
    hw2.add_weather(date.today(), dw3)
"""

#def test_add_weather():

def test_add_weather_date_exists():
    dw1 = DailyWeather((10, 5, 20), (16, -1, 12))
    dw2 = DailyWeather((5, -10, 15), (-1, -1, 5))
    dw3 = DailyWeather((6, -11, 17), (10, 3, 2))
    hw1 = HistoricalWeather('New York', (1, 2))
    hw1.add_weather(date.today(), dw1)
    hw1.add_weather(date.today(), dw2)
    hw1.add_weather(date.today(), dw3)
    assert hw1.__str__() == f'New York (1, 2):\n{date.today().strftime("%Y-%m-%d")}: Average: 10 Low: 5 High: 20 Precipitation: 16 Snow: 12 Rain: -1'

#def test_retrieve_weather():


def test_retrieve_weather_no_date():
    dw1 = DailyWeather((10, 5, 20), (16, -1, 12))
    hw1 = HistoricalWeather('New York', (1, 2))
    hw1.add_weather(date.today(), dw1)
    assert hw1.retrieve_weather(date(2020, 6, 1)) is None


def test_record_high_if_tie():
    dw1 = DailyWeather((10, 5, 20), (16, -1, 12))
    dw2 = DailyWeather((10, 5, 20), (16, -1, 12))
    hw1 = HistoricalWeather('New York', (1, 2))
    hw1.add_weather(date.today(), dw1)
    hw1.add_weather(date(1999, 2, 5), dw2)
    assert hw1.record_high(2, 5)

#def test_monthly_average_none_for_some():

#def test_monthly_average_none_for_all():

#def test_contiguous_precipitation_when_tie():

#def test_contiguous_precipitation_when_zero():

#def test_percentage_snowfall_no_snowfall():

#def test_percentage_snowfall_with_trace_amounts():

#def test_country_init_and_str():

#def test_add_history():

#def test_add_history_when_location_exists():

#def test_retrieve_history():

#def test_retrieve_history_when_no_location():

#def test_snowiest_location_when_tie():

#def test_snowiest_location_when_none():

#def test_snowiest_location_when_empty():


def test_load_data_random_lines_match_expected():
    with open('weather_data/small_sample_data.csv') as source:
        historical_weather = load_data(source)
        assert historical_weather.retrieve_weather(date(2017, 3, 11)).precipitation == -1

def test_load_data_omits_ill_formed_lines():
    with open('weather_data/test_sample_data.csv') as source:
        historical_weather = load_data(source)
        assert historical_weather.retrieve_weather(date(2020,5,17)) is None
        assert historical_weather.retrieve_weather(date(2020,12,24)) is not None

def test_load_data_converts_trace_amounts():
    with open('weather_data/small_sample_data.csv') as source:
        historical_weather = load_data(source)
        assert historical_weather.retrieve_weather(date(2020, 12, 30)).snowfall == -1

if __name__ == '__main__':
    pytest.main(['tests.py'])
