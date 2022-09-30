# https://www.youtube.com/watch?v=dam0GPOAvVI&list=WL&index=47   36:08
from website import create_app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)