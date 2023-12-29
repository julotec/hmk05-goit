import platform
import aiohttp
import asyncio
from datetime import datetime, timedelta


async def fetch_exchange_rate(session, date): #importuje kursy dla określonej daty
    url = f"https://api.nbp.pl/api/exchangerates/tables/a/{date}?format=json"
    async with session.get(url) as response:
        if response.status == 200:  #sprawdza czy żadanie zakończyło się sukcesem
            result = await response.json() #odczytuje dane JSON z odpowiedzi i oczekuje że operacja zakończy się
            return result[0]['rates'] #chcemy uzyskać piewszy element z listy, rates odwołuje się do key rates, który jest pierwszym elementem na liście
        else:
            return None #zwraca None jeśli żądanie się nie powiodło


async def main():
    async with aiohttp.ClientSession() as session: #asynchroniczny kontekst sesji HTTP
        exchange_rates = [] # lista, która będzie przechowywała kursy wymiany
        for i in range(10, 0, -1): #pętla iterujaca po ostatich 10 dniach
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            rates = await fetch_exchange_rate(session, date)
            if rates:
                exchange_rates.append({date: {'EUR': {'sale': rates[0]['mid'], 'purchase': rates[0]['mid']},
                                              'USD': {'sale': rates[1]['mid'], 'purchase': rates[1]['mid']}}})
        return exchange_rates


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.get_event_loop() 
    result = loop.run_until_complete(main()) 
    print(result)



