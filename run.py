from app import create_app


app=create_app("development")

if __name__== '__main__':
    app.run()



# celery_app=make_celery(app)
# app.run(host="0.0.0.0",port=443,ssl_context=("domain.crt","domain.key"))

# app.run("0.0.0.0")
# app.run("0.0.0.0",8000)
# app.run(debug=True)
# app.run(threaded=True)
# app.run(host="0.0.0.0",port=8686)

