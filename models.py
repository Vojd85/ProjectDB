class Material:
    def __init__(self, id, plan, name, type, mat, size, count, length, comments):
        self.id = id
        self.plan = plan
        self.name = name
        self.type = type
        self.mat = mat
        self.size = size
        self.count = count
        self.length = length
        self.comments = comments


class Record:
    def __init__(self, id, plan, name, type, mat, size, count, length, weigth, date, invoice, requirement, order, plan_order, master, receive, worker):
        self.id = id
        self.plan = plan
        self.name = name
        self.type = type
        self.mat = mat
        self.size = size
        self.count = count
        self.length = length
        self.weigth = weigth
        self.date = date
        self.invoice = invoice
        self.requirement = requirement
        self.order = order
        self.plan_order = plan_order
        self.master = master
        self.receive = receive
        self.worker = worker


class User:
    def __init__(self, surname, level, id, active):
        self.surname = surname
        self.level = level
        self.id = id
        self.active = active