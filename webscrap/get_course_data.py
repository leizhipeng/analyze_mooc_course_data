from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import codecs
import os

class get_course_data:
    """
    A class to get course data from course webpage.
    """
    def __init__(self,inputfile0,output_directory0):
        """
        Initialize class with input file and output directory.
        :param inputfile0: input file.
        :param output_directory0: output directory.
        """
        with open(inputfile0) as file:
            content = file.readlines()
        self.links = [item.split('\t')[2] for item in content[1:]]
        self.output_directory = output_directory0

        # self.driver = webdriver.Edge()
        # self.driver=webdriver.Chrome()
        self.driver = webdriver.Firefox()

    def get_data(self,k):
        """
        Get data of the k-th course.
        :param k: course number.
        """
        product_link=self.links[k]
        self.driver.get(product_link)
        time.sleep(30)

        course_file_name0 = self.output_directory+str(k+1)+"_info.txt"
        course_file_name1 = self.output_directory+str(k+1)+"_instructor.txt"
        course_file_name2 = self.output_directory+str(k+1)+"_review.txt"


        try:
            title= self.driver.find_element_by_class_name("clp-lead__title").text
            title= re.sub('[^A-Za-z0-9_]', ' ', title)
        except:
            return
        try:
            headline = self.driver.find_element_by_class_name("clp-lead__headline").text
            headline= re.sub('\t\n\r', '', headline)
        except:
            headline = "NULL"

        try:
            enrollment = self.driver.find_elements_by_xpath("//div[@data-purpose='enrollment']")
            enrollment = re.sub(',', '', enrollment[1].text)
            enrollment =re.sub("[^0-9]", '', enrollment)
        except:
            enrollment = "NULL"

        try:
            ratings_a = self.driver.find_element_by_xpath("//div[@class='styles--rating-wrapper--5a0Tr']").text
            rating = ratings_a.split('\n')[1]
            num_ratings = ratings_a.split('\n')[2]
            num_ratings=re.sub("[^0-9]", '', num_ratings)
        except:
            num_ratings = "NULL"   
            rating = "NULL"     

        try:
            last_update_date = self.driver.find_element_by_xpath("//div[@data-purpose='last-update-date']").text
            last_update_date= re.sub('Last updated ', '', last_update_date)
        except:
            last_update_date = "NULL"        

        try:
            what_you_get = self.driver.find_element_by_class_name("what-you-will-learn--content-spacing--3btHJ").text
            what_you_get= re.sub('[^A-Za-z0-9_]', ' ', what_you_get)
        except:
            what_you_get = "NULL"

        try:
            requirements = self.driver.find_element_by_class_name("ud-component--course-landing-page-udlite--requirements").text
            requirements = re.sub('[^A-Za-z0-9_]', ' ', requirements)
        except:
            requirements = "NULL"

        try:
            description = self.driver.find_element_by_xpath("//div[@data-purpose='course-description']").text
            description= re.sub('\n', ' ', description)
            description= re.sub('\t', ' ', description)
        except:
            description = "NULL"

        try:
            stars = self.driver.find_elements_by_class_name("review-summary-widget--rate-percent--2dtfO")
            five_stars = stars[0].text
            four_stars = stars[1].text
            three_stars = stars[2].text
            two_stars = stars[3].text
            one_star = stars[4].text
        except:
            five_stars = "NULL"
            four_stars = "NULL"
            three_stars = "NULL"
            two_stars = "NULL"
            one_star = "NULL"

        try:
            other_info = self.driver.find_element_by_class_name("incentives--incentives-container--CUQ8q").text
        except:
            other_info = "NULL"

        f0 = codecs.open(course_file_name0, 'w', encoding='utf8')
        f1 = codecs.open(course_file_name1, 'w', encoding='utf8')
        f2 = codecs.open(course_file_name2, 'w', encoding='utf8')

        f0.write(str(k+1)+'\n')
        f0.write(title + '\n')
        f0.write(headline +'\n')
        f0.write(enrollment +'\n')
        f0.write(rating +'\n')
        f0.write(num_ratings +'\n')
        f0.write(last_update_date +'\n')
        f0.write(what_you_get +'\n')
        f0.write(requirements +'\n')
        f0.write(description +'\n')

        f0.write(five_stars +'\n')
        f0.write(four_stars +'\n')
        f0.write(three_stars +'\n')
        f0.write(two_stars +'\n')
        f0.write(one_star +'\n')

        f0.write(other_info + "\n")

        instructors= self.driver.find_elements_by_class_name("instructor--instructor--1wSOF")
        for instructor in instructors:
            try:
                instructor_title = instructor.find_element_by_xpath("div/div[@class='udlite-heading-lg instructor--instructor__title--34ItB']").text
                instructor_job_title = instructor.find_element_by_xpath("div/div[@class='udlite-text-md instructor--instructor__job-title--1HUmd']").text
                tmp = instructor.find_elements_by_xpath("div/ul/li")
                instructor_rating = tmp[0].text
                instructor_no_reviews = tmp[1].text
                instructor_no_students = tmp[2].text
                instructor_no_courses = tmp[3].text
                instructor_info = instructor.find_element_by_xpath("div[3]").text
                instructor_info = re.sub('\n', ' ', instructor_info)
            except:
                instructor_title = "NULL"
                instructor_job_title = "NULL"
                instructor_rating = "NULL"
                instructor_no_reviews = "NULL"
                instructor_no_students = "NULL"
                instructor_no_courses = "NULL"
                instructor_info = "NULL"

        f1.write(instructor_title +'\n')
        f1.write(instructor_job_title +'\n')
        f1.write(instructor_rating +'\n')
        f1.write(instructor_no_courses +'\n')
        f1.write(instructor_no_reviews +'\n')
        f1.write(instructor_no_students +'\n')
        f1.write(instructor_info +'\n')

        reviews = self.driver.find_elements_by_class_name("reviews-section--review-container--3F3NE")
        for item in reviews:
            try:
                review_rating = item.find_element_by_xpath("div/div/div/span/span[@class='udlite-sr-only']").text
                review_rating = re.findall(r"[-+]?\d*\.\d+|\d+", review_rating)[0]
            except:
                review_rating = "NULL"
            
            try:
                review = item.find_element_by_xpath("div/div[@class='individual-review--individual-review-content--en4c7']/div[3]").text
                review = re.sub('\n', ' ', review)
            except:
                review = "NULL"

            f2.write(review_rating +'\n'+review+'\n')

        f0.close()
        f1.close()
        f2.close()

    def run(self):
        """
        Run the web scrapping.
        """
        for k in range(495,len(self.links)):
            self.get_data(k)
        self.driver.quit()

if __name__ == "__main__":
    # Specify the ranking file.
    file = "course_list.tsv"
    # Specify the output file.
    output_directory = '../data/raw/'

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    course = get_course_data(file, output_directory)
    course.run()
