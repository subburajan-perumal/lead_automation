from app import main


app=main.create_app()
app.run("0.0.0.0")
# app.run("0.0.0.0",8000)
# app.run()
# app.run(threaded=True)
# app.run(host="0.0.0.0",port=8686)
