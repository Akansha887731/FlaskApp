from flask import Flask, render_template
app = Flask(__name__)

posts = [{
    'heading': "My Blog 1",
    'content': "This is my first blog post. Welcome to my blog!",
    'author': "John Doe"},
    {
    'heading': "My Blog 2",
    'content': "This is my second blog post. Hope you enjoy reading!",  
    'author': "Jane Smith"
    }
    ]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts, title='Home Page')


@app.route('/about')
def about():
    return render_template('about.html', title='About Page')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
