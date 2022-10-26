from flask import Flask, render_template, request
from model import main

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    show = True # generate button visibility to reduce GPT usage
    ooo = False # message indicator if GPT fails or no money
    if request.method == 'POST':
        bites, links = main()
        show = False
        if bites == links:
            ooo = True
    else:
        bites, links = ([],[])
        #l = 1
    bite_link = zip(bites, links)
    return render_template('index.html', bl=bite_link, show_button=show, ooo_msg=ooo)


if __name__ == '__main__':
    app.run(use_reloader = True, debug = True)