def scrap(web_url):
    from requests_html import HTMLSession
    session = HTMLSession()
    r = session.get(web_url)
    content = r.html.xpath('//*[@id="article-content"]')
    # print("SITE - ", web_url)
    content = content[0].text
    import re
    prediction = re.split('Edited', content)
    print(re.findall(r'Prediction:.*', prediction[0]))


if __name__ == "__main__":
    print("Handy Scrapper Tool")
    matches = [
        'Sweden vs Slovakia',
        'Croatia vs Czech Republic',
        'England vs Scotland',
        'Hungary vs France',
        'Portugal vs Germany',
        'Spain vs Poland',
        'Italy vs Wales',
        'Switzerland vs Turkey'
    ]

    for match in matches:
        print('=-=-=' * 5 + match + '=-=-=' * 5)

        website_url = 'https://www.sportskeeda.com/football/' \
                      '{match}-prediction-preview-team-news-uefa-euro-2020'.format(
            match='-'.join(match.split()).lower())

        website1_url = 'https://www.sportskeeda.com/football/rumor-' \
                       '{match}-prediction-preview-team-news-uefa-euro-2020'.format(
            match='-'.join(match.split()).lower())

        try:
            scrap(website_url)
        except:
            try:
                print("ERROR ")
                scrap(website1_url)
            except:
                print("ERROR2 :(")
