from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# def scrape_stock_data(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     rows = soup.find_all('tr')
#     stock_data = []
#     for row in rows:
#         symbol_element = row.find('a', class_='Fw(600) C($linkColor)')
#         if symbol_element:
#             symbol = symbol_element.text.strip()
#         else:
#             continue
#         name_element = row.find('td', class_='Va(m) Ta(start) Px(10px) Fz(s)')
#         if name_element:
#             name = name_element.text.strip()
#         else:
#             continue
#         price_element = row.find('fin-streamer')
#         if price_element:
#             price = price_element.text.strip()
#         else:
#             continue
#         stock_data.append({'symbol': symbol, 'name': name, 'price': price})
#     return stock_data


def scrape_stock_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('tr')
    stock_data = []
    for row in rows:
        symbol_element = row.find('a', class_='Fw(600) C($linkColor)')
        if symbol_element:
            symbol = symbol_element.text.strip()
        else:
            continue

        name_element = row.find('td', class_='Va(m) Ta(start) Px(10px) Fz(s)')
        if name_element:
            name = name_element.text.strip()
        else:
            continue

        price_element = row.find('fin-streamer')
        if price_element:
            price = price_element.text.strip()
        else:
            continue

        # Extract image URL
        symbol_img_element = row.find(
            'img', class_='W(20px) H(20px) Mend(5px)')
        if symbol_img_element:
            symbol_img_url = symbol_img_element['src']
        else:
            symbol_img_url = None

        stock_data.append({'symbol': symbol, 'name': name,
                          'price': price, 'img_url': symbol_img_url})
    return stock_data


@app.route('/')
def crypto():
    crypto_url = "https://finance.yahoo.com/crypto/"
    crypto_data = scrape_stock_data(crypto_url)
    return render_template('index.html', stocks=crypto_data)


@app.route('/stocks')
def index():
    most_active_url = "https://finance.yahoo.com/most-active/"
    most_active_data = scrape_stock_data(most_active_url)
    return render_template('index.html', stocks=most_active_data)


@app.route('/gainers')
def gainers():
    gainer_url = "https://finance.yahoo.com/gainers/"
    gainer_data = scrape_stock_data(gainer_url)
    return render_template('index.html', stocks=gainer_data)


@app.route('/losers')
def losers():
    loser_url = "https://finance.yahoo.com/losers/"
    loser_data = scrape_stock_data(loser_url)
    return render_template('index.html', stocks=loser_data)


if __name__ == '__main__':
    app.run(debug=True)
