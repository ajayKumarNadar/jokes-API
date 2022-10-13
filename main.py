from flask import Flask, render_template, request
import requests

URL = "https://v2.jokeapi.dev/joke/Any"
req_url = "https://v2.jokeapi.dev/joke/Any"
filter_dict = {
    "Programming": True,
    "Miscellaneous": True,
    "Dark": True,
    "Pun": True,
    "Spooky": True,
    "Christmas": True,
    "single": True,
    "twopart": True,
    "nsfw": False,
    "religious": False,
    "political": False,
    "racist": False,
    "sexist": False,
    "explicit": False
}

app = Flask(__name__)


def create_url():
    if filter_dict["Programming"] == filter_dict["Miscellaneous"] == filter_dict["Dark"] == filter_dict["Pun"] == \
            filter_dict["Spooky"] == filter_dict["Christmas"]:
        return URL
    else:
        category_dict = {
            "Programming": filter_dict["Programming"],
            "Miscellaneous": filter_dict["Miscellaneous"],
            "Dark": filter_dict["Dark"],
            "Pun": filter_dict["Pun"],
            "Spooky": filter_dict["Spooky"],
            "Christmas": filter_dict["Christmas"]
        }
        new_url = URL.replace("Any", "")
        for key in category_dict:
            if category_dict[key]:
                new_url += f"{key},"
        new_url = new_url[:-1]
        return new_url


def create_param():

    # Blacklist
    blacklist_dict = {
        "nsfw": filter_dict["nsfw"],
        "religious": filter_dict["religious"],
        "political": filter_dict["political"],
        "racist": filter_dict["racist"],
        "sexist": filter_dict["sexist"],
        "explicit": filter_dict["explicit"]
    }
    blacklist = ""
    for key in blacklist_dict:
        if blacklist_dict[key]:
            blacklist += f"{key},"
    blacklist_param = blacklist[:-1]

    # Type
    if filter_dict['single'] == filter_dict['twopart']:
        filter_dict['single'] = True
        filter_dict['twopart'] = True
        return {
            "blacklistFlags": blacklist_param
        }
    elif filter_dict['single']:
        type_param = "single"
    else:
        type_param = "twopart"

    # Return param
    return {
        "blacklistFlags": blacklist_param,
        "type": type_param
    }


@app.route("/", methods=['GET', 'POST'])
def home():
    global filter_dict, req_url

    if request.method == 'POST':
        filter_data = request.form
        for key in filter_dict:
            filter_dict[key] = False
        for data in filter_data:
            filter_dict[data] = True

        req_url = create_url()
        req_parameter = create_param()

        response = requests.get(url=req_url, params=req_parameter).json()
        return render_template("index.html", filter_dict=filter_dict, joke=response)

    response = requests.get(url=req_url).json()
    return render_template("index.html", filter_dict=filter_dict, joke=response)


if __name__ == '__main__':
    app.run(debug=True)
