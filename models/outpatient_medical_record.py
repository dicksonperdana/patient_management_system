from odoo import models, api, fields, _
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from odoo.api import Environment as env


class OutpatientAssessment(models.Model):
    _name = "outpatient.record"
    _rec_name = "mr_id"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    @api.depends('birth_date')
    @api.one
    def onchange_age(self):
        if self.birth_date:
            dt = self.birth_date
            d1 = datetime.strptime(dt, "%Y-%m-%d").date()
            d2 = datetime.today()
            rd = relativedelta(d2, d1)
            self.patient_age = str(rd.years) + "y" + " " + str(rd.months) + "m" + " " + str(rd.days) + "d"
        else:
            self.patient_age = "Date of Birth is Empty"

    @api.onchange('nursing_assessment_line')
    def check_nursing_line(self):
        if len(self.nursing_assessment_line) > 1:
            raise ValidationError(_('Number of nursing assessment document exceed the limit'))

    @api.onchange('doctor_assessment_line')
    def check_doctor_line(self):
        if len(self.doctor_assessment_line) > 1:
            raise ValidationError(_('Number of doctor assessment document exceed the limit'))

    @api.constrains('nursing_assessment_line')
    def check_nursing_line_constrains(self):
        if len(self.nursing_assessment_line) > 1:
            raise ValidationError(_('Silahkan hapus dokumen yang terakhir ditambahkan'))

    @api.constrains('doctor_assessment_line')
    def check_doctor_line_constrains(self):
        if len(self.doctor_assessment_line) > 1:
            raise ValidationError(_('Silahkan hapus dokumen yang terakhir ditambahkan'))

    @api.one
    def action_done(self):
        if len(self.doctor_assessment_line) >= 1:
            self.state = 'done'
            vals = {'is_medical_record': True, 'state': 'done'}
            appointment = self.env['hospital.appointment'].browse(self.appointment_ids)
            write = appointment.sudo().write(vals)
            return write
        else:
            raise ValidationError('Asesmen harus terisi')

    def action_assessment(self):
        for rec in self:
            rec.state = 'assessment'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    @api.onchange('patient_id')
    def clinic_parent(self):
        for rec in self:
            path_clinic = self.env['ir.config_parameter'].sudo().get_param('patient_management_system.path_clinic_name')
            return {'domain': {'clinic': [('parent_id', '=', path_clinic)]}}

    mr_id = fields.Char(string="ID")
    is_invoiced = fields.Boolean(copy=False, default=False)
    nursing_assessment_line = fields.One2many('outpatient.nursing.record', 'medical_record_id',
                                              string='Nursing Assesment')
    doctor_assessment_line = fields.One2many('outpatient.doctor.record', 'medical_record_id',
                                             string='Doctor Assesment')
    diagnostic_document_line = fields.One2many('outpatient.diagnostic.document', 'medical_record_id',
                                               string='Diagnostic Document')
    assessment_date = fields.Date(string="Tanggal pemeriksaan")
    # appointment_id = fields.Many2one('hospital.appointment', string='Appointment', required=True)
    appointment_ids = fields.Integer(string='Appointment')
    patient_id = fields.Many2one('patient.record', string='Patient', required=True)
    clinic = fields.Many2one('hr.department', string="Klinik Tujuan")
    no_rm = fields.Char(string="No RM", related="patient_id.no_rm")
    birth_date = fields.Date(string='Tanggal Lahir', related="patient_id.date_of_birth", readonly=True)
    patient_age = fields.Char(string="Umur saat kunjungan", compute=onchange_age, store=True, readonly=True)
    allergic_history = fields.Text(string="Riwayat Alergi")
    birth_place = fields.Char(string="Tempat Lahir", related='patient_id.birth_place')
    address = fields.Text(string="Alamat", related="patient_id.address")
    phone = fields.Char(string="No Telp", related='patient_id.phone')
    sex = fields.Selection([('m', 'Male'), ('f', 'Female')], string="Jenis Kelamin", related="patient_id.sex")
    suku = fields.Char(string='Suku/Bangsa')
    education = fields.Selection(
        [('TS', 'Tidak Sekolah'), ('SD', 'Sekolah Dasar'), ('SMP', 'Menengah Pertama'), ('SMA', 'Menengah Atas'),
         ('S1', 'Sarjana'), ('S2', 'Magister'), ('S3', 'Doktor')], string='pendidikan', related='patient_id.education')
    job_status = fields.Selection([('PNS', 'Pegawai Negeri'), ('SW', 'Swasta')], string="Pekerjaan",
                                  related='patient_id.job_status')
    economic_status = fields.Selection([('1', 'Baik'), ('2', 'Cukup'), ('3', 'Kurang')], string="Status Ekonomi")
    religion = fields.Selection([('Islam', 'Islam'), ('Katolik', 'Katolik')], string="Agama",
                                related='patient_id.religion')
    state = fields.Selection([
        ('draft', 'Draft'), ('assessment', 'Assessment'), ('done', 'Done'), ('cancel', 'Cancelled')],
        string='Status', default='draft', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('mr_id', _('New')) == _('New'):
            vals['mr_id'] = self.env['ir.sequence'].next_by_code('medical.record.sequence') or _('New')
        result = super(OutpatientAssessment, self).create(vals)
        return result

    has_attachments = fields.Boolean('Has Attachments', compute='_compute_has_attachments')

    @api.one
    @api.depends('mr_id')
    def _compute_has_attachments(self):
        nbr_attach = self.env['ir.attachment'].search_count(
            [('res_model', '=', 'outpatient.record'), ('res_id', '=', self.id)])
        self.has_attachments = bool(nbr_attach)

    @api.multi
    def action_see_attachments(self):
        domain = [('res_model', '=', 'outpatient.record'), ('res_id', '=', self.id)]
        attachment_view = self.env.ref('patient_management_system.view_document_file_kanban_outpatient')
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': attachment_view.id,
            'views': [(attachment_view.id, 'kanban'), (False, 'form')],
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Click to upload files to your product.
                    </p><p>
                        Use this feature to store any files, like drawings or specifications.
                    </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % ('outpatient.record', self.id)
        }


class OutpatientNursingAssessment(models.Model):
    _name = "outpatient.nursing.record"
    _description = "Nursing Assessment"
    _rec_name = "nursing_assessment_id"

    @api.depends('patient_weight', 'patient_height')
    def _onchange_bmi(self):
        if self.patient_height != 0:
            meters = self.patient_height / 100
            bmi = self.patient_weight / (meters*meters)
            self.bmi = bmi
        else:
            self.bmi = 0

    user_id = fields.Many2one('res.users', string='Perawat Penanggung Jawab',
                              required=True,
                              index=True,
                              readonly=True,
                              default=lambda self: self.env.uid)

    nursing_assessment_id = fields.Char(string="ID", required=True, copy=False, readonly=True, index=True,
                                        default=lambda self: _('New'))
    medical_record_id = fields.Many2one('outpatient.record', string='Medical Record')
    patient_id = fields.Many2one('patient.record', string='Patient', related='medical_record_id.patient_id',
                                 readonly=True)
    general_condition = fields.Selection(
        [('1', 'Tampak Tidak Sakit'), ('2', 'Sakit Ringan'), ('3', 'Sakit Sedang'), ('4', 'Sakit Berat')],
        string='Keadaan umum')
    consciousness = fields.Selection(
        [('1', 'Compos Mentis'), ('2', 'Apatis'), ('3', 'Somnolen'), ('3', 'Sopor'), ('4', 'Coma')])
    glasgow_coma_scale_e = fields.Selection([('0', 'Not Testable'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')],
                                            string='E')
    glasgow_coma_scale_m = fields.Selection(
        [('0', 'Not Testable'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], string='M')
    glasgow_coma_scale_v = fields.Selection(
        [('0', 'Not Testable'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], string='V')
    patient_weight = fields.Float(string='Berat Badan (Kg)')
    patient_height = fields.Float(string='Tinggi Badan (cm)')
    blood_pressure = fields.Float(string='Tekanan Darah (mmHg)')
    vein = fields.Float(string='Nadi (x/mnt)')
    breath = fields.Float(string='Pernapasan (x/mnt)')
    body_temperature = fields.Float(string='Suhu Tubuh (C)')
    pain = fields.Selection([('1', 'Ada'), ('2', 'Tidak Ada')], default='2', string="Assessmen Nyeri")
    provokatif = fields.Char(string='Provokatif')
    quality = fields.Char(string='Quality')
    region = fields.Char(string='Lokasi')
    spread = fields.Char(string='Menyebar')
    severity = fields.Char(string='Severity')
    duration = fields.Char(string='Durasi')
    disapear_if = fields.Text(string='Menghilang Jika')
    fall_risk = fields.Selection([('1', 'Tidak'), ('2', 'Ya')], string='Resiko Jatuh')
    bmi = fields.Float(string="BMI (Kg/M3)", compute=_onchange_bmi)
    head_circle = fields.Float(string='Lingkar Kepala')
    support_tools = fields.Text(string='Alat Bantu')
    prothesis = fields.Text(string='Prothesis')
    defect = fields.Text(string='Cacat Tubuh')
    adl = fields.Selection([('1', 'Mandiri'), ('2', 'Dibantu')], string='ADL')

    persarafan_line = fields.One2many('nurse.persarafan.line', 'nursing_assessment_id', strinng="Persarafan")
    pernafasan_line = fields.One2many('nurse.pernapasan.line', 'nursing_assessment_id', strinng="Pernafasan")
    pencernaan_line = fields.One2many('nurse.pencernaan.line', 'nursing_assessment_id', strinng="Pencernaan")
    endorkin_line = fields.One2many('nurse.endorkin.line', 'nursing_assessment_id', strinng="Endorkin")
    kardiovaskuler_line = fields.One2many('nurse.kardiovaskuler.line', 'nursing_assessment_id', strinng="Kardiovaskuler")
    abdomen_line = fields.One2many('nurse.abdomen.line', 'nursing_assessment_id', strinng="Abdomen")
    reproduksi_line = fields.One2many('nurse.reproduksi.line', 'nursing_assessment_id', strinng="Reproduksi")
    kulit_line = fields.One2many('nurse.kulit.line', 'nursing_assessment_id', strinng="Kulit")
    urinaria_line = fields.One2many('nurse.urinaria.line', 'nursing_assessment_id', strinng="Urinaria")
    mata_line = fields.One2many('nurse.mata.line', 'nursing_assessment_id', strinng="Mata")
    ost_line = fields.One2many('nurse.ost.line', 'nursing_assessment_id', strinng="Otot, Sendi, dan Tulang")
    muka_line = fields.One2many('nurse.muka.line', 'nursing_assessment_id', strinng="Muka")
    gigi_line = fields.One2many('nurse.gigi.line', 'nursing_assessment_id', strinng="Gigi")
    telinga_line = fields.One2many('nurse.telinga.line', 'nursing_assessment_id', strinng="Telinga")
    tenggorokan_line = fields.One2many('nurse.tenggorokan.line', 'nursing_assessment_id', strinng="Tenggorokan")
    emosional_line = fields.One2many('nurse.emosional.line', 'nursing_assessment_id', strinng="Emosional")

    @api.model
    def create(self, vals):
        if vals.get('nursing_assessment_id', _('New')) == _('New'):
            vals['nursing_assessment_id'] = self.env['ir.sequence'].next_by_code('nursing.assessment.sequence') or _(
                'New')
        result = super(OutpatientNursingAssessment, self).create(vals)
        return result


class OutpatientDoctorAssessment(models.Model):
    _name = "outpatient.doctor.record"
    _description = "Doctor Assessment"
    _rec_name = "doctor_assessment_id"

    @api.onchange('user_id')
    def clinic_parent(self):
        for rec in self:
            path_clinic = self.env['ir.config_parameter'].sudo().get_param('patient_management_system.path_clinic_name')
            return {'domain': {'consultation': [('parent_id', '=', path_clinic)]}}

    user_id = fields.Many2one('res.users', string='Doctor Responsible',
                              required=True,
                              index=True,
                              readonly=True,
                              default=lambda self: self.env.uid)

    doctor_assessment_id = fields.Char(string="ID", required=True, copy=False, readonly=True, index=True,
                                       default=lambda self: _('New'))
    medical_record_id = fields.Many2one('outpatient.record', string='Medical Record')
    patient_id = fields.Many2one('patient.record', string='Patient', related='medical_record_id.patient_id',
                                 readonly=True)
    medical_service_line_ids = fields.Many2many('medical.service.line', 'doctor_assessment_id', string='Tindakan')
    # medical_service_line_ids = fields.Many2many('hospital.icd9', string='Tindakan')
    medical_diagnose_line_ids = fields.One2many('medical.diagnose.line', 'doctor_assessment_id', string='Diagnosa')
    # medical_diagnose_line_ids = fields.Many2many('hospital.icd10', string='Diagnosa')

    main_complaint = fields.Text(string='Keluhan Utama', required=True)
    disease_history = fields.Text(string='Riwayat penyakit')
    physical_examination = fields.Text(string="Pemeriksaan Fisik")
    pediatric_nutrition = fields.Text(string='Status Gizi')
    pediatric_immunization_history = fields.Text(string='Riwayat Imunisasi')
    pediatric_growth = fields.Text(string='Riwayat Tumbuh Kembang')
    status_lokalis = fields.Text(string='Status Lokalis')
    support_checkup = fields.Text(string='Pemeriksaan Penunjang')
    therapy = fields.One2many('hospital.drugs.line.mr', 'doctor_assessment_id', string='Terapi')
    # therapy = fields.One2many('hospital.drugs', string='Terapi')
    consultation = fields.Many2many('hr.department', string="Konsultasi")
    refer = fields.Text(string='Dirujuk')
    patient_handling = fields.Selection([('1', 'Pulang'), ('2', 'Dirawat'), ('3', 'Menolak Dirawat'), ('4', 'Dirujuk')],
                                        string='Penanganan Pasien')
    is_invoiced = fields.Boolean(copy=False, default=False)
    is_signature = fields.Binary(string="Tanda Tangan", required=True)

    @api.model
    def create(self, vals):
        if vals.get('doctor_assessment_id', _('New')) == _('New'):
            vals['doctor_assessment_id'] = self.env['ir.sequence'].next_by_code(
                'doctor.assessment.sequence') or _('New')
        result = super(OutpatientDoctorAssessment, self).create(vals)
        return result


class OutpatientDiagnosticAssessment(models.Model):
    _name = "outpatient.diagnostic.document"
    _rec_name = "document_id"

    medical_record_id = fields.Many2one('outpatient.record', string='Medical Record')
    document_id = fields.Char(string="Document ID", required=True, copy=False, readonly=True, index=True,
                              default=lambda self: _('New'))
    file = fields.Binary(string='file', filename="name", attachment=True)
    name = fields.Char(string="Deskripsi")

    @api.model
    def create(self, vals):
        if vals.get('document_id', _('New')) == _('New'):
            vals['document_id'] = self.env['ir.sequence'].next_by_code(
                'diagnostic.document.sequence') or _('New')
        result = super(OutpatientDiagnosticAssessment, self).create(vals)
        return result
