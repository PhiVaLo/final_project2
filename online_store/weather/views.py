from django.shortcuts import render

from . utils import get_html_content

from store.utils import cartData


# Create your views here.
def weather(request):

    weather_data = {}
    unknown_location = {}
    try:
        if 'city' in request.GET:
            # Fetch weather data
            city = request.GET.get('city')
            html_content = get_html_content(city)

            # Scraping
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Weather of the week (7 days)
            def weather_week(day):
                dayy = soup.find('div', attrs={'data-wob-di': day}).find('div', attrs={'class': 'QrNVmd Z1VzSb'}).text
                logo = soup.find('div', attrs={'data-wob-di': day}).find('img', attrs={'class': 'uW5pk'})['src']
                min_temp = soup.find('div', attrs={'data-wob-di': day}).find('div', attrs={'class': 'QrNVmd ZXCv8e'}).find('span', attrs={'style': 'display:inline'}).text
                max_temp = soup.find('div', attrs={'data-wob-di': day}).find('div', attrs={'class': 'vk_gy gNCp2e'}).find('span', attrs={'style': 'display:inline'}).text
                return [dayy, logo, min_temp, max_temp]

            for i in range(7):
                weather_data['day' + str(i)] = weather_week(str(i))[0]
                weather_data['logo' + str(i)] = weather_week(str(i))[1]
                weather_data['min_temp' + str(i)] = weather_week(str(i))[2]
                weather_data['max_temp' + str(i)] = weather_week(str(i))[3]

            # Current weather status
            weather_data.update({
                'region': soup.find('div', attrs={'id': 'wob_loc'}).text,

                'daytime': soup.find('div', attrs={'id': 'wob_dts'}).text,
                'status': soup.find('span', attrs={'id': 'wob_dc'}).text,
                'logo': soup.find('img', attrs={'id': 'wob_tci'})['src'],
                'temp': soup.find('span', attrs={'id': 'wob_tm'}).text,

                'precipitation': soup.find('span', attrs={'id': 'wob_pp'}).text,
                'humidity': soup.find('span', attrs={'id': 'wob_hm'}).text,
                'wind': soup.find('span', attrs={'id': 'wob_ws'}).text,
            })
    except:
        unknown_location = {'input': request.GET.__getitem__('city')}


    # cart data
    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'weather': weather_data,
        'unknown_location': unknown_location,
        'cartItems': cartItems,
    }
    return render(request, 'weather/weather_api.html', context)