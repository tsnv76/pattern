from views import Index, About, Contacts, Otchets

# Набор привязок: путь-контроллер
routes = {
    '/': Index(),
    '/about/': About(),
    '/contacts/': Contacts(),
    '/otchets/': Otchets(),
}

