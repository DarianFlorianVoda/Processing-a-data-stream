import requests
import getpass
def download_file():
    username = getpass.getuser()
    file_url = 'https://data.gov.ro/dataset/b86a78a3-7f88-4b53-a94f-015082592466/resource/d0b60b45-fb08-4980-a34c-8cbb4a43cad3/download/transparenta_martie_2021.xlsx'

    print('Beginning file download with urllib2...')
    file_object = requests.get(file_url)

    with open('COVID-19.xlsx', 'wb') as local_file:
        local_file.write(file_object.content)

download_file()

