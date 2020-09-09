from bs4 import BeautifulSoup
import requests
import csv


def get_html(url):
    r = requests.get(url)
    if r.ok: 
        return r.text
    else: 
        print("Code is ", r.status_code)


def write_csv(data):
    with open("avito.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow((data['name'],data['price'], data['text']))


def get_current_page(soup, current=None): # GEt current page
    for page in soup.find(attrs={'data-marker':'pagination-button'}).find_all('span'):
        for attrs in page.get('class'):
            if attrs.rfind('pagination-item_active') != -1:
                current = int(page.text)
                break
        if current: break
    return current


def prev_page(html):
    """ The function calculate a current page 
    Then return №page-1 to URL """
    # First get current page
    soup = BeautifulSoup(html, 'lxml') 
    current = get_current_page(soup)
    # If current == 1 it's first page
    if current == 1:
        pass # Need return error
    return current - 1 # Return preview page 


def next_page(html):
    soup = BeautifulSoup(html, 'lxml') 
    current = get_current_page(soup)
    if len(soup.find(attrs={'data-marker':'pagination-button/next'}).get('class')) == 3:
        print("LAST PAGE SUKA")
    return current+1



def get_page_data(html, index=0):
    # Get data from the page
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find('div', class_='snippet-list').find_all('div', class_='snippet')
    print("Items: ", soup.find(attrs={'data-marker':'page-title/count'}))
    print("And items len on the page is ", len(items))
    actions = ['next', 'back', 'check', 'exit'] # Action list

    while True:
        try:
            print(items[index].find('div', class_="item_table-wrapper").find('div', class_='description').h3.text[2:-2])
            print(index)
            response = input("Action: ")
        except:
            print("Out of list")
            break
        # [next, back, check, exit]
        if response in actions:
            if response == 'next':
                index += 1
                if index == 50:
                    return 'np'
                elif index == len(items):
                    index -=1 
                    print("It's last item")
            elif response == 'back':
                index -= 1
                if index == -1:
                    return 'bp'
            elif response == 'check':
                u = items[index].find('a',class_='snippet-link').get('href')
                # print('Url is ', u)     
                result = BeautifulSoup(get_html("https://www.avito.ru/"+u), 'lxml')
                name = result.find('span', class_='title-info-title-text').text
                print(name)
                price = result.find(attrs={'itemprop':'price'}).text
                text = result.find('div',class_='item-description').text
                data = {
                    'name':name,
                    'price':price,
                    'text':text
                }
                write_csv(data)
                
            else: 
                print("GoodBye, suka")
                break
        else: 
            print("I do not know what do you mean\n")

    # Action after 


    print("GoodBye")


def get_page(pattern, country, query, page=1):
    url = pattern.format(country, page, query)
    index = 0
    while True: 
        html = get_html(url)
        action = get_page_data(html, index)
        if action == 'np': # NextPage
            print("\nNEXT PAGE\n")
            page = next_page(html)
            index = 0
        elif action == 'bp':
            print("\nPREV PAGE\n")
            page = prev_page(html) # back page data
            index = 49 
        url = pattern.format(country, page, query)
                    


def main():
    pattern = "https://www.avito.ru/{}?p={}&q={}"
    query = input("Введите запрос: ")
    country = "volgograd"

    get_page(pattern, country, query)

    # url = pattern.format(query)
    # get_page_data(get_html(url))

    # for i in range(48):
    #     get_page_data(get_html(url))
    #     print("{} Page is done".format(i+1))


if __name__ == "__main__":
    main()