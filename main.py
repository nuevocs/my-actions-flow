import httpx
from selectolax.parser import HTMLParser
import pandas as pd

from dataclasses import dataclass, asdict
@dataclass
class GameSales:
    rank: int
    title: str
    console: str
    publisher: str
    duration: str
    start_date: str
    end_date: str

url = "https://www.famitsu.com/ranking/game-sales/"
resp = httpx.get(url)

html = HTMLParser(resp.text)
games = html.css("div.card.card-game-sale-rank.card-game-sale-rank--col-12.card-game-sale-rank--col-sm-12.card-game-sale-rank--col-md-12.card-game-sale-rank--col-lg-8")
duration = html.css_first('span.heading__sub-text-body').text().replace("年", "/").replace("月","/").replace("日","")
start_date = duration.split("～")[0]
end_date = duration.split("～")[1]

results = []
for item in games:
    new_item = GameSales(
    title=item.css_first("div.card-game-sale-rank__title").text(),
    rank=item.css_first("span.icon-ranking").text(),
    console=item.css_first("span.icon-console").text(),
    publisher=item.css_first("p.card-game-sale-rank__publisher").text(),
    duration=duration,
    start_date=start_date,
    end_date=end_date
    )
    results.append(asdict(new_item))

df = pd.DataFrame(data=results, columns=['rank', 'title', 'console', 'publisher', 'duration', 'start_date','end_date'])
df.to_csv("famidata.csv", index=False)
