import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def money(number: int, grouping: bool = True, lang=1):
    return f"{locale.currency(number, grouping=grouping).split('.')[0][1:]}"



   """
            <!-- {% for i in text_uz %}
                <div class="col-6">
                    <div class="card-body">
                    <div class="form-floating">
                        <input type="text" class="form-control" id="floatingInput" placeholder="John Doe" aria-describedby="floatingInputHelp">
                        <label for="floatingInput">{{i.data}}</label>
                    </div>
                    </div>
                    </div>
                {% endfor %} -->

            <!-- <div class="col-6">
                <div class="card-body">
                <div class="form-floating">
                    <input type="text" class="form-control" id="floatingInput" placeholder="John Doe" aria-describedby="floatingInputHelp">
                    <label for="floatingInput">ru</label>
                </div>
                </div>
                </div>
                <div class="col-6">
                <div class="card-body">
                <div class="form-floating">
                    <input type="text" class="form-control" id="floatingInput" placeholder="John Doe" aria-describedby="floatingInputHelp">
                    <label for="floatingInput">ru</label>
                </div>
                </div>
                </div> -->
    """
