from bs4 import BeautifulSoup
import requests
import re
import pymongo


class Bus:

    def __init__(self):
        self.key = 'KCCmg%2BFH81e74ptCVObbpItzvOWSM2dX1EDlZfXckrKdJUAS6DtQhI9VoIQCD9gUHRtIQ4Oo%2Br1Ph5YJIqVWlw%3D%3D'
        self.Bus_url = 'http://ws.bus.go.kr/api/rest/pathinfo/getPathInfoByBus'  # 경로
        self.station_url = 'http://ws.bus.go.kr/api/rest/pathinfo/getLocationInfo'  # 정류장 정보 검색
        self.ArrivalStation_url = 'http://ws.bus.go.kr/api/rest/arrive/getArrInfoByRouteAll'
        self.startX, self.startY, self.endX, self.endY = '', '', '', ''
        self.start_station = ''
        self.end_station = ''

        self.routeRouteId = ''

    def FindRoute(self):
        findUrl = self.Bus_url + '?serviceKey=' + self.key + '&startX=' + self.startX + '&startY=' + self.startY \
                  + '&endX=' + self.endX + '&endY=' + self.endY

        res = requests.get(findUrl)
        soup = BeautifulSoup(res.content, 'html.parser')

        # 버스번호 (환승필요시 2개 이상의 버스 리스트 출력) 데이터타입 = list
        routeBusNumber = re.compile(r"\d+\w").findall(str(soup.select_one('itemlist').select('pathList>routeNm')))

        # 노선번호 (환승필요시 2개 이상의 버스 리스트 출력) 데이터타입 = list
        self.routeRouteId = re.compile(r"\d+\w").findall(str(soup.select_one('itemlist').select('pathList>routeId')))

        # 탑승 ,하차 정류장 (환승 필요시 리스트 출력) 데이터타입 = list
        routeStationId = re.compile(r"(?<=\>)[A-Za-z0-9가-힣]+").findall(
            str(soup.select_one('itemlist').select('pathList>fname, tname')))

        client = pymongo.MongoClient(
            "mongodb+srv://Main:1q2w3e4r@cluster0.dbjal.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority")
        db = client.get_database('Register')
        db.get_collection('Bus').insert_one({'Reservation': str(routeBusNumber), 'station': str(routeStationId)})

        # 버스 번호, 탑승 하차 정류장
        return ''.join(routeBusNumber)

    def FindStation(self, a, b):
        self.start_station = a
        self.end_station = b
        # 출발 정류장 번호 parse
        start_stationUrl = self.station_url + '?serviceKey=' + self.key + '&stSrch=' + self.start_station
        start_res = requests.get(start_stationUrl)
        start_soup = BeautifulSoup(start_res.content, 'html.parser')

        # 출발 정류장 번호
        self.startX = re.findall(r"\d+.\d+", str(start_soup.select_one('gpsX')))[0]
        self.startY = re.findall(r"\d+.\d+", str(start_soup.select_one('gpsY')))[0]

        """print("출발 정류장번호", re.findall(r"\d+.\d+", str(start_soup.select_one('poiId')))[0])"""

        # 도착 정류장 번호 parse
        end_stationUrl = self.station_url + '?serviceKey=' + self.key + '&stSrch=' + self.end_station
        end_res = requests.get(end_stationUrl)
        end_soup = BeautifulSoup(end_res.content, 'html.parser')
        # 도착 정류장 번호
        self.endX = re.findall(r"\d+.\d+", str(end_soup.select_one('gpsX')))[0]
        self.endY = re.findall(r"\d+.\d+", str(end_soup.select_one('gpsY')))[0]

        """print("도착 정류장번호", re.compile(r"\d+.\d+").findall(str(end_soup.select('poiId')))[0])
        print("좌표", self.startX, self.startY, self.endX, self.endY)"""
