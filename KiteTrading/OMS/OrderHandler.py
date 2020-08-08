from OMS.Order import Order

orders = []


def add_order(order):
    if order is not None:
        orders.add(order)
        return 1
    print('Order not found')
    return -1


def remove_order(order):
    if order is not None:
        if order in orders:
            orders.remove(order)
            return 1
    print('Order not found')
    return -1


def update_order_status(client, order):
    if order is not None:
        if order in orders:
            # todo request status from kite
            orders[orders.index(order)].status = order.status
            return 1
    return -1

