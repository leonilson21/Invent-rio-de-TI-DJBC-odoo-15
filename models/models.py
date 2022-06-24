from odoo import models, fields, api
import requests
import logging
_logger = logging.getLogger(__name__)

class DJBCCategs(models.Model):
    _name='djbc.categs'
    _description='DJBC Categories'
    _rec_name='name'

    name = fields.Text(string='DJBC Category', required=True,)

class DJBCHSCode(models.Model):
    _name='djbc.hscode'
    _description='DJBC HS Code'
    _rec_name='code'

    code = fields.Char(string='HS Code', required=True,)
    name = fields.Text(string='HS Description', required=True,)



class DJBCDocType(models.Model):
    _name='djbc.doctype'
    _description='DJBC Document Type'
    _rec_name='code'

    code = fields.Char(string='Doc. Type', required=True,)
    is_import_doc = fields.Boolean(string='Is an Import Document?', required=True, default=False)

class DJBCContainers(models.Model):
    _name='djbc.containers'
    _description='DJBC Containers'
    _rec_name='name'

    name = fields.Char(string='Container No', required=True,)
    container_size = fields.Char(string='Size', required=False,)
    container_type = fields.Char(string='Type', required=False,)
    gate_pass = fields.Char(string='Gate Pass', required=False,)
    doc_id = fields.Many2one(comodel_name="djbc.docs", string="DJBC Doc", required=False, )

class DJBCDocs(models.Model):
    _name='djbc.docs'
    _description='DJBC Documents'
    _rec_name='no_dok'

    no_dok = fields.Char(string='Nomor Dokumen BC', required=True,)
    tgl_dok = fields.Date(string='Tanggal Dokumen BC', required=True,)
    jenis_dok = fields.Many2one(comodel_name="djbc.doctype", string="Doc Type", required=True, )
    no_aju = fields.Char(string="Nomor Pengajuan", required=False, )
    tgl_aju = fields.Date(string="Tanggal Pengajuan", required=False, )
    no_bl = fields.Char(string="Nomor B/L", required=False, )
    tgl_bl = fields.Date(string="Tanggal B/L", required=False, )
    jenis_bl = fields.Selection(
        string="Jenis B/L",
        selection=[
            ("master", "Master"),
            ("house", "House"),
        ],
        required=False,
        default="house",
    )
    no_cont = fields.Char(string="Nomor Container", required=False, )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("req_do", "DO Request"),
            ("wait_do", "DO Invoiced"),
            ("paid_do", "DO Paid"),
            ("sent_do", "DO Sent"),
            ("req_sp2", "SP2 Request"),
            ("wait_sp2", "SP2 Invoiced"),
            ("paid_sp2", "SP2 Paid"),
            ("sent_sp2", "SP2 Sent"),
        ],
        required=True,
        default="draft",
    )

    kd_document_type = fields.Integer(string="Kode Document Type", required=False, )
    npwpCargoOwner = fields.Char(string='NPWP Cargo Owner', required=False, )
    # npwpCargoOwner = fields.Many2one(comodel_name="res.partner", string="NPWP Cargo Owner", required=True, )
    nm_cargoowner = fields.Many2one(comodel_name="res.partner", string="Nama Cargo Owner", required=False,
                                    domain=[('nle_category', '=', 'consignee'),])
    no_doc_release = fields.Char(string='Doc Release No', required=False,)
    date_doc_release = fields.Date(string='Doc Release Date', required=False,)
    document_state = fields.Char(string='Document Status', required=False,)
    id_platform = fields.Char(string='Id Platform', required=False, default='XXXXX')
    # terminal = fields.Char(string='Terminal', required=False,)
    terminal = fields.Many2one(comodel_name="res.partner", string="Terminal", required=False,
                               domain=[('nle_category', '=', 'terminal'), ])
    paid_thrud_date = fields.Date(string='Paid Date', required=False,)
    proforma = fields.Char(string='Proforma', required=False,)
    price = fields.Float(string="Price",  required=False, )
    proforma_date = fields.Date(string='Proforma Date', required=False,)
    sent_sp2_date = fields.Date(string='Tgl Kirim SP2', required=False, )
    status = fields.Char(string='Status', required=False,)
    is_finished = fields.Boolean(string='Is Finished?', required=False, default=False)
    party = fields.Integer(string='Jumlah Container', required=False, )
    keterangan = fields.Text(string="Keterangan", required=False, )
    container_ids = fields.One2many(comodel_name="djbc.containers", inverse_name="doc_id",string="Container List", required=False, )

    # tambahan dari DO
    request_date = fields.Date(string='Request DO Date', required=False, )
    request_date_sp2 = fields.Date(string='Request SP2 Date', required=False, )
    id_ff_ppjk = fields.Char (string='NPWP FF/PPJK', required=False, )
    # shipping_name = fields.Char (string='Shipping Line', required=False, )
    shipping_name = fields.Many2one(comodel_name="res.partner", string="Shipping Name", required=False,
                    domain=[('nle_category', '=', 'shipping'), ])
    forwarder_name = fields.Many2one(comodel_name="res.partner", string="Nama FF/PPJK", required=False,
                                    domain=[('nle_category', '=', 'ppjk'),])
    price_do = fields.Float(string='Price DO', required=False, )
    paid_date_do = fields.Date(string='Paid Date DO', required=False, )
    status_do = fields.Char(string='Status DO', required=False, )

    do_number = fields.Char(string='Nomor DO', required=False, )
    do_date_number = fields.Date(string='Tgl DO', required=False, )
    sent_do_date = fields.Date(string='Tgl Kirim DO', required=False, )

    @api.onchange('nm_cargoowner')
    # @api.multi
    def onchange_nm_cargoowner(self):
        self.npwpCargoOwner = self.nm_cargoowner.vat

    @api.onchange('forwarder_name')
    # @api.multi
    def onchange_forwarder_name(self):
        self.id_ff_ppjk = self.forwarder_name.vat

class DJBCProductTemplate(models.Model):
    _inherit='product.template'

    hscode = fields.Many2one(comodel_name="djbc.hscode", string="HS Code", required=False, )
    djbc_category_id = fields.Many2one(comodel_name="djbc.categs", string="Extra Category", required=False, )

# class DJBCStockInventory(models.Model):
#     _inherit='stock.inventory'
#     djbc_mark=fields.Boolean(string='DJBC Marking') 

class DJBCStockLocation(models.Model):
    _inherit='stock.location'

    is_stock_location = fields.Boolean(string="Is a Stock Location?",  )
    street = fields.Char(string="Street",  )
    city = fields.Char(string="City",  )

class DJBCStockMove(models.Model):
    _inherit='stock.move'

    djbc_masuk_flag = fields.Boolean(string='DJBC Masuk')
    djbc_keluar = fields.Boolean(string='DJBC Keluar')
    sisa_qty = fields.Float(string='Sisa Qty')
    jumlah_kemasan = fields.Float(string="Jumlah Kemasan", required=False, )
    satuan_kemasan = fields.Char(string="Satuan Kemasan", required=False, )

class DJBCStockPicking(models.Model):
    _inherit='stock.picking'

    docs_id = fields.Many2one(string='DJBC Document',comodel_name='djbc.docs',)

    def action_assign(self):
        res = super(DJBCStockPicking, self).action_assign()
        # raise UserError(self.location_dest_id)
        if (self.picking_type_id.name=='Pick Components'):
            for rec in self.move_line_ids_without_package:
                # spl = self.env['stock.production.lot'].browse(rec.lot_id.id)
                rec.location_dest_id=self.location_dest_id
        return res

class DJBCStockPickingType(models.Model):
    _inherit='stock.picking.type'

    move_type = fields.Selection([('in','in'),('out','out'),],string='Move Type', required=False,)


