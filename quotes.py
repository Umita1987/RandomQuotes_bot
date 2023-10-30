import httpx


class RandomFamousQuotes:

    def __init__(self):
        pass

    @staticmethod
    async def get_quotes(category, count):
        url = "https://andruxnet-random-famous-quotes.p.rapidapi.com/"
        querystring = {"cat": category, "count": count}

        headers = {
            "X-RapidAPI-Key": "9692f46630msh94a8cfef7514347p1dabb2jsn67b604229313",
            "X-RapidAPI-Host": "andruxnet-random-famous-quotes.p.rapidapi.com"
        }

        response = httpx.get(url, headers=headers, params=querystring)
        data = response.json()
        quotes = []
        for i in range(len(data)):
            quotes.append(str(data[i]["quote"]) + " " + str(data[i]["author"]))
        return "\n".join(quotes)



