import platform
import aiohttp
import asyncio
from datetime import datetime, timedelta


async def fetch_exchange_rates(session, start_date, end_date):  # importuje kursy dla określonego zakresu dat
    url = f"https://api.nbp.pl/api/exchangerates/tables/a/{start_date}/{end_date}?format=json"
    async with session.get(url) as response:
        if response.status == 200:  # sprawdza czy żądanie zakończyło się sukcesem
            result = await response.json()  # odczytuje dane JSON z odpowiedzi i oczekuje że operacja zakończy się
            return result[0]['rates']  # chcemy uzyskać pierwszy element z listy, rates odwołuje się do key rates, który jest pierwszym elementem na liście
        else:
            return None  # zwraca None jeśli żądanie się nie powiodło


async def main():
    async with aiohttp.ClientSession() as session:  # asynchroniczny kontekst sesji HTTP
        exchange_rates = []  # lista, która będzie przechowywała kursy wymiany
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')

        rates = await fetch_exchange_rates(session, start_date, end_date)
        if rates:
            for rate in rates:
                date = rate['effectiveDate']
                exchange_rates.append({date: {'EUR': {'sale': rate['mid'], 'purchase': rate['mid']},
                                              'USD': {'sale': rate['mid'], 'purchase': rate['mid']}}})
        return exchange_rates


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.get_event_loop()  # pobiera obiekt pętli asynchronicznej
    result = loop.run_until_complete(main())  # uruchamia funkcję main i czeka na jej zakończenie
    print(result)



