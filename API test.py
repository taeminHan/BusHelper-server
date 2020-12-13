from bs4 import BeautifulSoup
import requests
import re

class Bus:

    def __init__(self):
        self.key = 'KCCmg%2BFH81e74ptCVObbpItzvOWSM2dX1EDlZfXckrKdJUAS6DtQhI9VoIQCD9gUHRtIQ4Oo%2Br1Ph5YJIqVWlw%3D%3D'
        self.Bus_url = 'http://ws.bus.go.kr/api/rest/pathinfo/getPathInfoByBus'  # 경로
        self.station_url = 'http://ws.bus.go.kr/api/rest/pathinfo/getLocationInfo'  #정류장 정보 검색
        self.startX, self.startY, self.endX, self.endX = '', '', '', ''

    def FindRoute(self):

        findUrl = self.Bus_url + '?serviceKey=' + self.key + '&startX=' + self.startX + '&startY=' + self.startY + '&endX=' + self.endX + '&endY=' + self.endY

        res = requests.get(findUrl)
        soup = BeautifulSoup(res.content, 'html.parser')

        print(re.findall(r"\d+", str(soup.select('routeNm')))[0])
        print(re.findall(r"\d+", str(soup.select('routeId')))[0])

    def FindStation(self, start_station, end_station):

        stationUrl = self.station_url + '?serviceKey=' + self.key + '&stSrch=' + start_station
        res = requests.get(stationUrl)
        soup = BeautifulSoup(res.content, 'html.parser')

        self.startX = re.findall(r"\d+.\d+", str(soup.select_one('gpsX')))[0]
        self.startY = re.findall(r"\d+.\d+", str(soup.select_one('gpsY')))[0]

        stationUrl = self.station_url + '?serviceKey=' + self.key + '&stSrch=' + end_station
        res = requests.get(stationUrl)
        soup = BeautifulSoup(res.content, 'html.parser')

        self.endX = re.findall(r"\d+.\d+", str(soup.select_one('gpsX')))[0]
        self.endY = re.findall(r"\d+.\d+", str(soup.select_one('gpsY')))[0]


a = Bus()
a.FindStation('성산2교', '홍대입구')
a.FindRoute()
