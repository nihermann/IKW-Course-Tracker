from typing import List, Tuple, Type, T

from selenium.webdriver.remote.webelement import WebElement


class Course:
    # todo get into for example SQLAlchemy to save this class into a db without much translation

    @classmethod
    def from_web_element(cls: Type[T], element: WebElement) -> T:
        """
        Extracts all information from the WebElement of one course entry.
        :param element: the respective WebElement
        :return: an instance of Course with all information set.
        """
        c = Course()
        c.course_vpv = element.get_attribute("course_vpv")
        c.title = element.get_attribute("course_title")
        c.term = element.get_attribute("course_term")
        c.year = element.get_attribute("course_year")
        c.type = element.find_element_by_class_name("course_type").text
        c.teachers = element.find_element_by_class_name("teachers").text

        hours_and_etcs = element.find_elements_by_class_name("col_left")[2].text.split("\n")
        c.week_hours = int(hours_and_etcs[0].split("h")[0])
        c.etcs = int(hours_and_etcs[1].split(" ")[0])

        modules = element.find_element_by_class_name("modules").text
        c.bachelor_modules, c.master_modules = _retrieve_modules(modules)

        c.is_doctorate_program = "Doctorate program" in modules

        c.timeslots = element.find_element_by_class_name("timeslots").text.split("\n")

        return c

    @classmethod
    def from_web_elements(cls: Type[T], elements: List[WebElement]) -> List[T]:
        return [cls.from_web_element(elem) for elem in elements]


def _retrieve_modules(modules: str) -> Tuple[List[str], List[str]]:
    """
    Separates bachelor and master modules in to two lists.
    :param modules: str returned from html containing all modules.
    :return: Tuple of two lists (bachelor_modules, master_modules)
    """
    ba_modules, ma_modules = [], []
    current_list = None
    no_category = False
    for m in modules.split("\n"):
        if "B.Sc" in m:
            current_list = ba_modules
        elif "M.Sc" in m:
            current_list = ma_modules
        elif m == "" or current_list is None:  # current_list is None if there were no BA/MA modules
            no_category = True
        elif no_category:
            if "Bachelor" in m:
                ba_modules.append(m)
            elif "Master" in m:
                ma_modules.append(m)
        else:
            if "Doctorate program" in m:
                continue
            current_list.append(m)

    return ba_modules, ma_modules
