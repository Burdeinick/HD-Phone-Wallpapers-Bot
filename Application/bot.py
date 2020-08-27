from flask import Flask, request


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def receive_update():
    if request.method == "POST":
        print(request.json)
    return {"ok": True}



# curl --location --request POST 'https://api.telegram.org/bot1389628186:AAFwom4Tc69Me6lbm_Iwv3RHIqK3AvzEYGs/setWebhook' \
# --header 'Content-Type: application/json' \
# --data-raw '{
#     "url": "https://501e3667b616.ngrok.io"
# }'
# ngrok http 5000
