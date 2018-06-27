class DBRouter(object):

    def db_for_read(self, model, **hints):
        if model._meta.db_table in ('orders', 'refund', 'pay_channel_info', 'pay_merchant_info', 'service_config'):
            return 'pay'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.db_table in ('orders', 'refund', 'pay_channel_info', 'pay_merchant_info', 'service_config'):
            return 'pay'
        return 'default'
