from odoo import models, api, fields, _


class NursePersarafan(models.Model):
    _name = "nurse.persarafan"
    _rec_name = "name_persarafan"

    name_persarafan = fields.Char(string="Deskripsi")

class NursePernapasan(models.Model):
    _name = "nurse.pernapasan"
    _rec_name = "name_pernapasan"

    name_pernapasan = fields.Char(string="Deskripsi")

class NursePencernaan(models.Model):
    _name = "nurse.pencernaan"
    _rec_name = "name_pencernaan"

    name_pencernaan = fields.Char(string="Deskripsi")

class NurseEndorkin(models.Model):
    _name = "nurse.endorkin"
    _rec_name = "name_endorkin"

    name_endorkin = fields.Char(string="Deskripsi")

class NurseKardiovaskuler(models.Model):
    _name = "nurse.kardiovaskuler"
    _rec_name = "name_kardiovaskuler"

    name_kardiovaskuler = fields.Char(string="Deskripsi")

class NurseAbdomen(models.Model):
    _name = "nurse.abdomen"
    _rec_name = "name_abdomen"

    name_abdomen = fields.Char(string="Deskripsi")

class NurseReproduksi(models.Model):
    _name = "nurse.reproduksi"
    _rec_name = "name_reproduksi"

    name_reproduksi = fields.Char(string="Deskripsi")

class NurseKulit(models.Model):
    _name = "nurse.kulit"
    _rec_name = "name_kulit"

    name_kulit = fields.Char(string="Deskripsi")

class NurseUrinaria(models.Model):
    _name = "nurse.urinaria"
    _rec_name = "name_urinaria"

    name_urinaria = fields.Char(string="Deskripsi")

class NurseMata(models.Model):
    _name = "nurse.mata"
    _rec_name = "name_mata"

    name_mata = fields.Char(string="Deskripsi")

class NurseOST(models.Model):
    _name = "nurse.ost"
    _rec_name = "name_ost"
    _description="Otot, Sendi, dan Tulang"

    name_ost = fields.Char(string="Deskripsi")

class NurseMuka(models.Model):
    _name = "nurse.muka"
    _rec_name = "name_muka"

    name_muka = fields.Char(string="Deskripsi")

class NurseGigi(models.Model):
    _name = "nurse.gigi"
    _rec_name = "name_gigi"

    name_gigi = fields.Char(string="Deskripsi")

class NurseTelinga(models.Model):
    _name = "nurse.telinga"
    _rec_name = "name_telinga"

    name_telinga = fields.Char(string="Deskripsi")

class NurseTenggorokan(models.Model):
    _name = "nurse.tenggorokan"
    _rec_name = "name_tenggorokan"

    name_tenggorokan = fields.Char(string="Deskripsi")

class NurseEmosional(models.Model):
    _name = "nurse.emosional"
    _rec_name = "name_emosional"

    name_emosional = fields.Char(string="Deskripsi")

# =========================================================================================