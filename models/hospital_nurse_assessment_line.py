from odoo import models, api, fields, _


class NursePersarafanLine(models.Model):
    _name = "nurse.persarafan.line"

    nursing_assessment_id = fields.Many2one('outpatient.nursing.record')
    name_persarafan_line = fields.Many2one('nurse.persarafan', string="Deskripsi")
    deskripsi_lanjut_persarafan = fields.Char(string="Detail")


class NursePernapasanLine(models.Model):
    _name = "nurse.pernapasan.line"

    nursing_assessment_id = fields.Many2one('outpatient.nursing.record')
    name_pernapasan_line = fields.Many2one('nurse.pernapasan', string="Deskripsi")
    deskripsi_lanjut_pernapasan = fields.Char(string="Detail")


class NursePencernaanLine(models.Model):
    _name = "nurse.pencernaan.line"

    nursing_assessment_id = fields.Many2one('outpatient.nursing.record')
    name_pencernaan_line = fields.Many2one('nurse.pencernaan', string="Deskripsi")
    deskripsi_lanjut_pencernaan = fields.Char(string="Detail")


class NurseEndorkinLine(models.Model):
    _name = "nurse.endorkin.line"

    nursing_assessment_id = fields.Many2one('outpatient.nursing.record')
    name_endorkin_line = fields.Many2one('nurse.endorkin', string="Deskripsi")
    deskripsi_lanjut_endorkin = fields.Char(string="Detail")

# =====
class NurseKardiovaskulerLine(models.Model):
    _name = "nurse.kardiovaskuler.line"

    nursing_assessment_id = fields.Many2one('outpatient.nursing.record')
    name_kardiovaskuler_line = fields.Many2one('nurse.kardiovaskuler', string="Deskripsi")
    deskripsi_lanjut_kardiovaskuler = fields.Char(string="Detail")


class NurseAbdomenLine(models.Model):
    _name = "nurse.abdomen.line"

    nursing_assessment_id = fields.Many2one('outpatient.nursing.record')
    name_abdomen_line = fields.Many2one('nurse.abdomen', string="Deskripsi")
    deskripsi_lanjut_abdomen = fields.Char(string="Detail")


class NurseReproduksiLine(models.Model):
    _name = "nurse.reproduksi.line"

    nursing_assessment_id = fields.Many2one('outpatient.nursing.record')
    name_reproduksi_line = fields.Many2one('nurse.reproduksi', string="Deskripsi")
    deskripsi_lanjut_reproduksi = fields.Char(string="Detail")


class NurseKulitLine(models.Model):
    _name = "nurse.kulit.line"

    nursing_assessment_id = fields.Many2one('outpatient.nursing.record')
    name_kulit_line = fields.Many2one('nurse.kulit', string="Deskripsi")
    deskripsi_lanjut_kulit = fields.Char(string="Detail")


class NurseUrinariaLine(models.Model):
    _name = "nurse.urinaria.line"

    nursing_assessment_id = fields.Many2one('outpatient.nursing.record')
    name_urinaria_line = fields.Many2one('nurse.urinaria', string="Deskripsi")
    deskripsi_lanjut_urinaria = fields.Char(string="Detail")


class NurseMataLine(models.Model):
    _name = "nurse.mata.line"

    nursing_assessment_id = fields.Many2one('outpatient.nursing.record')
    name_mata_line = fields.Many2one('nurse.mata', string="Deskripsi")
    deskripsi_lanjut_mata = fields.Char(string="Detail")


class NurseOSTLine(models.Model):
    _name = "nurse.ost.line"
    _description = "Otot, Sendi, dan Tulang"

    nursing_assessment_id = fields.Many2one('outpatient.nursing.record')
    name_ost_line = fields.Many2one('nurse.ost', string="Deskripsi")
    deskripsi_lanjut_ost = fields.Char(string="Detail")


class NurseMukaLine(models.Model):
    _name = "nurse.muka.line"

    nursing_assessment_id = fields.Many2one('outpatient.nursing.record')
    name_muka_line = fields.Many2one('nurse.muka',string="Deskripsi")
    deskripsi_lanjut_muka = fields.Char(string="Detail")


class NurseGigiLine(models.Model):
    _name = "nurse.gigi.line"

    nursing_assessment_id = fields.Many2one('outpatient.nursing.record')
    name_gigi_line = fields.Many2one('nurse.gigi', string="Deskripsi")
    deskripsi_lanjut_gigi = fields.Char(string="Detail")

class NurseTelingaLine(models.Model):
    _name = "nurse.telinga.line"

    nursing_assessment_id = fields.Many2one('outpatient.nursing.record')
    name_telinga_line = fields.Many2one('nurse.telinga', string="Deskripsi")
    deskripsi_lanjut_telinga = fields.Char(string="Detail")

class NurseTenggorokanLine(models.Model):
    _name = "nurse.tenggorokan.line"

    nursing_assessment_id = fields.Many2one('outpatient.nursing.record')
    name_tenggorokan_line = fields.Many2one('nurse.tenggorokan', string="Deskripsi")
    deskripsi_lanjut_tenggorokan = fields.Char(string="Detail")

class NurseEmosionalLine(models.Model):
    _name = "nurse.emosional.line"

    nursing_assessment_id = fields.Many2one('outpatient.nursing.record')
    name_emosional_line = fields.Many2one('nurse.emosional', string="Deskripsi")
    deskripsi_lanjut_emosional = fields.Char(string="Detail")



