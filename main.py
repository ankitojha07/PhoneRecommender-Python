from recomnder import recomnder
from products import product

app = recomnder(size="1060x628", sizeLock = True)
app.AddHeader(heading="Mobile Recommender", fontStyle="Impact", fontSize=20)

app.AddFilterBar(width=32)
app.InsertFilter(name='Price', option=['<5,000', '5,000 - 10,000', '10,000 - 25,000', '25,000 - 50,000', '>50,000'])
app.InsertFilter(name='RAM', option=['6 GB', '4 GB', '3 GB'])
app.InsertFilter(name='Internal Storage', option=['256 GB', '128 GB', '64 GB', '32 GB', '16 GB'])
app.InsertFilter(name='Camera', option=['72MP', '64MP', '48MP', '32MP'])
app.InsertFilter(name="Brand", option=['Samsung', 'Xiaomi', 'Apple', 'Real me', 'Oppo'])

app.AddSearchBar()

app.AddBody(width=850)
for i in product:
    app.InsertItem(title=i['title'], image_url=i['image_url'], price=i['price'], features=i['features'])
app.ProductRegister(product)

app.ShowWindow()