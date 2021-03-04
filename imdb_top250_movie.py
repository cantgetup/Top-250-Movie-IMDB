import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from tqdm import tqdm


def create_imdb_movie_table():
    # open browser, headless
    option = webdriver.ChromeOptions()
    option.add_argument('headless')

    DRIVER_PATH = 'D:\ChromeDriver\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=option)
    driver.get('https://www.imdb.com/chart/top/')
        
    # create dataFrame
    imdb_movie_table = pd.DataFrame()
        
    # get all movie name anchor
    titles = driver.find_elements_by_xpath('//td[@class="titleColumn"]/a')
    
    # all titles
    list_titles = []

    for title in titles:
        tt = title.text
        list_titles.append(tt)

    # all url for movies
    list_links = []

    for title in titles:
        ll = title.get_attribute('href')
        list_links.append(ll[:ll.find('?')])

    # get director, writer, star, genre
    director_list = []
    writer_list = []
    star_list = []
    genre_list = []    
    
    for url in tqdm(list_links):
        the_info = get_movie_info(url)
        
        director_list.append(the_info[0])
        writer_list.append(the_info[1])
        star_list.append(the_info[2])
        genre_list.append(the_info[3])    
    
    
    # all ratings
    ratings = driver.find_elements_by_xpath('//td[contains(@class,"imdbRating")]')

    list_ratings = []

    for r in ratings:
        rr = r.text
        list_ratings.append(rr)

    imdb_movie_table['Title'] = list_titles
    imdb_movie_table['url'] = list_links
    
    imdb_movie_table['Director'] = director_list
    imdb_movie_table['Writer'] = writer_list
    imdb_movie_table['Star'] = star_list
    imdb_movie_table['Genre'] = genre_list
    
    imdb_movie_table['Rating'] = list_ratings
    
    return imdb_movie_table
  
def get_movie_info(url):

    option = webdriver.ChromeOptions()
    option.add_argument('headless')

    DRIVER_PATH = 'D:\ChromeDriver\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=option)
    driver.get(url)
    
    # find all div for 'credit_summary_item'
    credits = driver.find_elements_by_xpath('//div[@class="credit_summary_item"]')
    
    # intitialize 
    str_directors = ''
    str_writers = ''
    str_stars = ''    
    
    has_director = False
    has_writer = False
    has_star = False
    
    list_directors = []
    list_writers = []
    list_stars = []
    
    
    # for each 'credit_summary_item'
    # look at the h4 text
    # find all 'a' tag, get the text
    # append to list
    for line in credits:
        if 'Director' in line.find_element_by_xpath('.//h4').text:
            has_director = True
            
            director_names = line.find_elements_by_xpath('.//a')
            for director_name in director_names:
                list_directors.append(director_name.text.strip())

        if 'Writer' in line.find_element_by_xpath('.//h4').text:
            has_writer= True
            
            writer_names = line.find_elements_by_xpath('.//a')
            for writer_name in writer_names:
                if 'more credit' not in writer_name.text:
                    list_writers.append(writer_name.text.strip())          

        if 'Star' in line.find_element_by_xpath('.//h4').text:
            has_star = True
            
            star_names = line.find_elements_by_xpath('.//a')
            for star_name in star_names:
                if 'See full cast' not in star_name.text:
                    list_stars.append(star_name.text.strip())

    str_directors = ' | '.join(list_directors)
    str_writers = ' | '.join(list_writers)
    str_stars = ' | '.join(list_stars)                    
    

    # Genres
    str_genres = ''
    list_genres = []
    
    # get the div, h4 = genre, back to div   
    genre_div = driver.find_element_by_xpath(
    '//div[@class="see-more inline canwrap"]//h4[contains(text(),"Genre")]//ancestor::div[@class="see-more inline canwrap"]')
    
    # find all 'a' under genre
    a_genres = genre_div.find_elements_by_xpath('.//a')

    for a in a_genres:
        list_genres.append(a.text.strip())
    
    str_genres = ' | '.join(list_genres)
    
    return str_directors, str_writers, str_stars, str_genres 
  

imdb_table = create_imdb_movie_table()

def one_color_func(word=None, font_size=None, 
                   position=None, orientation=None, 
                   font_path=None, random_state=None):
    h = random_state.randint(250, 350) # 0 - 360
    s = random_state.randint(60, 100) # 0 - 100
    l = random_state.randint(15, 60) # 0 - 100
    return "hsl({}, {}%, {}%)".format(h, s, l)
  
def create_wordcloud(df, column_name):
    temp_list = []
    for cell in df[column_name]:
        temp_list.extend(cell.split(' | '))

    temp_list = [cell for cell in temp_list if cell != 'N/A']    

    # ranked by creators
    aa = Counter(temp_list)
    sorted_dict = sorted(aa.items(), key=lambda item: item[1], reverse=True)

    wc = WordCloud(background_color="yellow", color_func=one_color_func, width=1600, height=1200)
    wc.generate_from_frequencies(Counter(temp_list))
    plt.figure(figsize=(12,8))
    plt.imshow(wc)
    plt.axis('off')
    plt.show()
    
    return sorted_dict  

create_wordcloud(imdb_table, 'Director')

create_wordcloud(imdb_table, 'Writer')

create_wordcloud(imdb_table, 'Star')

create_wordcloud(imdb_table, 'Genre')
