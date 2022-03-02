from typing import List
import datetime

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.select import Select

from IKWScraper.Course import Course


def check_for_updates(headless=False) -> List[Course]:
    """
    Scrapes the ikw page and searches for new lectures.
    :return: The newly added lectures
    """
    options = Options()
    options.headless = headless
    # launch firefox
    driver = webdriver.Firefox(options=options)
    try:
        driver.get("https://www.ikw.uni-osnabrueck.de/en/courses_of_study/lectures.html")
        driver.switch_to.frame(driver.find_element_by_id("lectures-iframe"))

        # get dropdowns for the course filter
        term = Select(driver.find_element_by_id("filter_term"))
        year = Select(driver.find_element_by_id("filter_year"))

        # apply filter
        term.select_by_visible_text(_get_current_term())
        year.select_by_visible_text(_get_current_year())

        # get all courses
        all_courses = driver.find_elements_by_class_name("course_entry_div")

        # unfortunately the webpages filter will only make the false ones invisible
        # therefore, we get only the ones where the style is not set, bzw not set to invisible.
        queried_courses = [c for c in all_courses if not c.get_attribute("style")]

        # create objects from factory method
        courses = Course.from_web_elements(queried_courses)

        # todo compare courses to courses in the db for changes (by vpv)

        # todo insert new courses into db

        # todo return new courses (ignore changes/ updates of courses for now)

        print()

        # dummy return
        return courses[:2]
    finally:
        # close firefox again
        driver.close()


def _get_current_year() -> str:
    """Returns the current year as string"""
    return str(datetime.date.today().year)


def _get_current_term() -> str:
    """Returns whether we are in the WS or SS"""
    # todo make it dynamic
    return "SS"
