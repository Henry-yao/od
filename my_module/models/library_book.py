from odoo  import models,fields
# from odoo.addons import decimal_precision as dp

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'date_release desc,name'
    _rec_name = 'short_name'
# 显示日期%%%%
    name = fields.Char('Title',required=True)
    short_name = fields.Char('Short Title',required=True)
    date_release = fields.Date('Release Date')
    author_ids = fields.Many2many('res.partner',string='Authors')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id,"%s(%s)"%(record.name,record.date_release))
            )
            return result
# 新加字段
# class LibraryBook(models.Model):
#     cost_price = fields.Float(
#         'Book Cost',dp.get_precision('Book price')
#     )
    # short_name = fields.Char('Short Title')
    # notes = fields.Text('Internal Notes')
    # state = fields.Selection([('draft','Not Available'),('available','Available'),('lost','Lost')],'State')
    # description = fields.Html('Description')
    # cover = fields.Binary('Book Cover')
    # out_of_print = fields.Boolean('Out of print?')
    # date_release = fields.Date('Release Date')
    # date_updated = fields.Datetime('Last Updated')
    # pages = fields.Integer('Number of Pages')
    # reader_rating = fields.Float('Reader Average Rating',digits=(14,4), #Optional precision (total,decimals,))ßß

# 添加用于储存货币的字段
# class LibraryBook(models.Model):currency_id = fields.Many2one('res.currency',string='Currency')
# class LibraryBook(models.Model)

# ...
# class LibraryBook(models.Model):cost_price = fields.Float(
#     'Book Cost', dp.get_precision('Book Price))
#
#
# class LibraryBook(models.Model):
#     # ...
#     currency_id = fields.Many2one('res.currency', string='Currency')
#
#
# class LibraryBook(models.Model):
#     # ...
#     retail_price = fields.Monetary(
#         'Retail Price',
#         # optional: currency_field='currency_id',
#         )
#发行商多对一字段ß
# class LibraryBook(models.Model):
#     publisher_id = fields.Many2many('res.partner',string='Publisher',ondelete='set null',context{},domain=[],)
# class ResPartner(models.Model):
#     _inherit = 'res.partner'
#     published_book_ids = fields.One2many(
#         'library.book','publisher_id',string='published Books'
#     )