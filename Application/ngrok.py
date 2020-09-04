# it's sure working for webhook set
curl --location --request POST 'https://api.telegram.org/bot1389628186:AAFwom4Tc69Me6lbm_Iwv3RHIqK3AvzEYGs/setWebhook' \
--header 'Content-Type: application/json' \
--data-raw '{
     "url": "https://3358e2301211.ngrok.io"
}'

ngrok http 5000