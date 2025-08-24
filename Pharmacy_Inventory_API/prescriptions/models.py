class Prescription(models.Model):
    patient = models.ForeignKey(
        'medicines.Patient',
        on_delete=models.PROTECT,
        related_name='prescriptions'
    )
    prescribed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        limit_choices_to={'role': 'DOCTOR'}
    )