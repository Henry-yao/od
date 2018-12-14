# -*- coding: utf-8 -*-
import logging
import hashlib
import uuid
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class CFLicense(models.Model):
    _name = 'cf.license'
    _description = u"许可证内容"

    UUID = fields.Char(string=u"许可证唯一编号", help=u"许可证唯一ID，一般是系统自动生成且不允许更改。")
    user_name = fields.Char(string=u"用户名称", required=True, help=u"该授权用户的名称")
    machine_code = fields.Char(string=u"机器码", required=True, help=u"授权使用的机器码，也就是odoo运行所在服务器的机器码")
    sign = fields.Text(string=u"签名", help=u"许可证的签名，一般是UUID+user_name+machine_code+modules 然后再做SHA1HASH")
    module_ids = fields.One2many("cf.license.module", "license_id", string=u"授权使用模块", help=u"授权使用的模块")

    @api.model
    def create(self, vals):
        # 生成许可证唯一编号
        _uuid = str(uuid.uuid1())
        vals["UUID"] = _uuid

        #创建并写入数据库
        lic = super(CFLicense, self).create(vals)

        #对许可证内容进行签名
        _sign = lic._sign_lic()
        # lic.sign = _sign
        lic.write({
            "sign": _sign
        })

        return lic

    def _sign_lic(self):
        """
        对许可证进行签名
        :return:
        """
        lic = self.UUID+self.user_name+self.machine_code
        modules = self.module_ids.mapped("name")
        m = ",".join(modules)  # module1,module2,....
        lic = lic + m
        return hashlib.sha1(lic.encode("utf-8")).hexdigest()


class CFLicenseModule(models.Model):
    _name = "cf.license.module"
    _description = u"可授权模块"

    license_id = fields.Many2one("cf.license", string=u"所属license", ondelete="cascade")
    name = fields.Char(string=u"模块名称", required=True)
    note = fields.Char(string=u"模块说明")
