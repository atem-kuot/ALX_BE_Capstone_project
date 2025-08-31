import React, { useState, useEffect } from 'react';
import { Table, Button, Badge, Form, InputGroup, Card, Alert, Modal } from 'react-bootstrap';
import { FiSearch, FiPlus, FiEye, FiPrinter, FiClock, FiCalendar, FiUser, FiAlertTriangle } from 'react-icons/fi';

const Prescriptions = () => {
  const [prescriptions, setPrescriptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showNewPrescription, setShowNewPrescription] = useState(false);
  const [showViewModal, setShowViewModal] = useState(false);
  const [selectedPrescription, setSelectedPrescription] = useState(null);
  const [newPrescription, setNewPrescription] = useState({
    patientName: '',
    patientAge: '',
    patientGender: 'male',
    diagnosis: '',
    medicines: [
      { name: '', dosage: '', frequency: '', duration: '' }
    ]
  });

  // Mock data - replace with actual API call
  useEffect(() => {
    const fetchPrescriptions = async () => {
      try {
        // Simulate API call
        setTimeout(() => {
          const mockPrescriptions = [
            {
              id: 1,
              patientName: 'John Doe',
              patientAge: 35,
              patientGender: 'male',
              diagnosis: 'Acute Pharyngitis',
              status: 'pending',
              createdAt: '2023-08-30T14:30:00Z',
              medicines: [
                { name: 'Amoxicillin 500mg', dosage: '1', frequency: '8 hourly', duration: '7 days' },
                { name: 'Ibuprofen 200mg', dosage: '1', frequency: '8 hourly', duration: '5 days' }
              ]
            },
            {
              id: 2,
              patientName: 'Jane Smith',
              patientAge: 28,
              patientGender: 'female',
              diagnosis: 'Migraine',
              status: 'completed',
              createdAt: '2023-08-29T10:15:00Z',
              completedAt: '2023-08-29T10:30:00Z',
              medicines: [
                { name: 'Sumatriptan 50mg', dosage: '1', frequency: 'as needed', duration: 'max 2 per day' }
              ]
            }
          ];
          setPrescriptions(mockPrescriptions);
          setLoading(false);
        }, 800);
      } catch (error) {
        console.error('Error fetching prescriptions:', error);
        setLoading(false);
      }
    };

    fetchPrescriptions();
  }, []);

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewPrescription({
      ...newPrescription,
      [name]: value
    });
  };

  const handleMedicineChange = (index, field, value) => {
    const updatedMedicines = [...newPrescription.medicines];
    updatedMedicines[index] = {
      ...updatedMedicines[index],
      [field]: value
    };
    setNewPrescription({
      ...newPrescription,
      medicines: updatedMedicines
    });
  };

  const addMedicineField = () => {
    setNewPrescription({
      ...newPrescription,
      medicines: [
        ...newPrescription.medicines,
        { name: '', dosage: '', frequency: '', duration: '' }
      ]
    });
  };

  const removeMedicineField = (index) => {
    const updatedMedicines = [...newPrescription.medicines];
    updatedMedicines.splice(index, 1);
    setNewPrescription({
      ...newPrescription,
      medicines: updatedMedicines
    });
  };

  const handleSubmitPrescription = (e) => {
    e.preventDefault();
    // In a real app, you would make an API call here
    const newId = Math.max(...prescriptions.map(p => p.id), 0) + 1;
    const prescriptionToAdd = {
      ...newPrescription,
      id: newId,
      status: 'pending',
      createdAt: new Date().toISOString()
    };
    
    setPrescriptions([prescriptionToAdd, ...prescriptions]);
    setShowNewPrescription(false);
    resetForm();
  };

  const resetForm = () => {
    setNewPrescription({
      patientName: '',
      patientAge: '',
      patientGender: 'male',
      diagnosis: '',
      medicines: [
        { name: '', dosage: '', frequency: '', duration: '' }
      ]
    });
  };

  const viewPrescription = (prescription) => {
    setSelectedPrescription(prescription);
    setShowViewModal(true);
  };

  const getStatusBadge = (status) => {
    const variants = {
      pending: 'warning',
      completed: 'success',
      cancelled: 'danger'
    };
    return (
      <Badge bg={variants[status]} className="text-capitalize">
        {status}
      </Badge>
    );
  };

  const filteredPrescriptions = prescriptions.filter(prescription =>
    prescription.patientName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    prescription.diagnosis.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ minHeight: '300px' }}>
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="prescriptions">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Prescriptions</h2>
        <div className="d-flex gap-2">
          <div style={{ minWidth: '250px' }}>
            <InputGroup size="sm">
              <InputGroup.Text>
                <FiSearch />
              </InputGroup.Text>
              <Form.Control
                type="text"
                placeholder="Search prescriptions..."
                value={searchTerm}
                onChange={handleSearch}
              />
            </InputGroup>
          </div>
          <Button 
            variant="primary" 
            size="sm"
            onClick={() => setShowNewPrescription(true)}
          >
            <FiPlus className="me-1" /> New Prescription
          </Button>
        </div>
      </div>

      <Card>
        <Card.Body>
          {filteredPrescriptions.length === 0 ? (
            <Alert variant="info">No prescriptions found.</Alert>
          ) : (
            <div className="table-responsive">
              <Table hover className="align-middle">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Patient</th>
                    <th>Diagnosis</th>
                    <th>Medicines</th>
                    <th>Status</th>
                    <th className="text-end">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredPrescriptions.map((prescription) => (
                    <tr key={prescription.id}>
                      <td>
                        <div className="d-flex flex-column">
                          <small className="text-muted">
                            {new Date(prescription.createdAt).toLocaleDateString()}
                          </small>
                          <small className="text-muted">
                            {new Date(prescription.createdAt).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                          </small>
                        </div>
                      </td>
                      <td>
                        <div className="d-flex align-items-center">
                          <div className="me-2">
                            <div className="avatar-sm bg-primary bg-opacity-10 text-primary d-flex align-items-center justify-content-center rounded-circle">
                              <FiUser size={16} />
                            </div>
                          </div>
                          <div>
                            <h6 className="mb-0">{prescription.patientName}</h6>
                            <small className="text-muted">{prescription.patientAge} years, {prescription.patientGender}</small>
                          </div>
                        </div>
                      </td>
                      <td>{prescription.diagnosis}</td>
                      <td>
                        <div className="d-flex flex-wrap gap-1">
                          {prescription.medicines.map((med, idx) => (
                            <Badge key={idx} bg="light" text="dark" className="text-truncate" style={{ maxWidth: '120px' }}>
                              {med.name}
                            </Badge>
                          ))}
                        </div>
                      </td>
                      <td>{getStatusBadge(prescription.status)}</td>
                      <td className="text-end">
                        <Button 
                          variant="outline-primary" 
                          size="sm" 
                          className="me-2"
                          onClick={() => viewPrescription(prescription)}
                        >
                          <FiEye size={14} />
                        </Button>
                        <Button variant="outline-secondary" size="sm">
                          <FiPrinter size={14} />
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </div>
          )}
        </Card.Body>
      </Card>

      {/* New Prescription Modal */}
      <Modal show={showNewPrescription} onHide={() => setShowNewPrescription(false)} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>New Prescription</Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSubmitPrescription}>
          <Modal.Body>
            <div className="row mb-3">
              <div className="col-md-6">
                <Form.Group className="mb-3">
                  <Form.Label>Patient Name</Form.Label>
                  <Form.Control
                    type="text"
                    name="patientName"
                    value={newPrescription.patientName}
                    onChange={handleInputChange}
                    required
                  />
                </Form.Group>
              </div>
              <div className="col-md-3">
                <Form.Group className="mb-3">
                  <Form.Label>Age</Form.Label>
                  <Form.Control
                    type="number"
                    name="patientAge"
                    value={newPrescription.patientAge}
                    onChange={handleInputChange}
                    required
                  />
                </Form.Group>
              </div>
              <div className="col-md-3">
                <Form.Group className="mb-3">
                  <Form.Label>Gender</Form.Label>
                  <Form.Select
                    name="patientGender"
                    value={newPrescription.patientGender}
                    onChange={handleInputChange}
                    required
                  >
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </Form.Select>
                </Form.Group>
              </div>
            </div>

            <Form.Group className="mb-4">
              <Form.Label>Diagnosis</Form.Label>
              <Form.Control
                as="textarea"
                rows={2}
                name="diagnosis"
                value={newPrescription.diagnosis}
                onChange={handleInputChange}
                required
              />
            </Form.Group>

            <h5 className="mb-3">Medicines</h5>
            {newPrescription.medicines.map((medicine, index) => (
              <div key={index} className="border p-3 mb-3 rounded">
                <div className="row">
                  <div className="col-md-5">
                    <Form.Group className="mb-3">
                      <Form.Label>Medicine Name</Form.Label>
                      <Form.Control
                        type="text"
                        value={medicine.name}
                        onChange={(e) => handleMedicineChange(index, 'name', e.target.value)}
                        required
                      />
                    </Form.Group>
                  </div>
                  <div className="col-md-2">
                    <Form.Group className="mb-3">
                      <Form.Label>Dosage</Form.Label>
                      <Form.Control
                        type="text"
                        placeholder="e.g., 1 tablet"
                        value={medicine.dosage}
                        onChange={(e) => handleMedicineChange(index, 'dosage', e.target.value)}
                        required
                      />
                    </Form.Group>
                  </div>
                  <div className="col-md-2">
                    <Form.Group className="mb-3">
                      <Form.Label>Frequency</Form.Label>
                      <Form.Control
                        type="text"
                        placeholder="e.g., 8 hourly"
                        value={medicine.frequency}
                        onChange={(e) => handleMedicineChange(index, 'frequency', e.target.value)}
                        required
                      />
                    </Form.Group>
                  </div>
                  <div className="col-md-2">
                    <Form.Group className="mb-3">
                      <Form.Label>Duration</Form.Label>
                      <Form.Control
                        type="text"
                        placeholder="e.g., 7 days"
                        value={medicine.duration}
                        onChange={(e) => handleMedicineChange(index, 'duration', e.target.value)}
                        required
                      />
                    </Form.Group>
                  </div>
                  <div className="col-md-1 d-flex align-items-end">
                    {index > 0 && (
                      <Button 
                        variant="outline-danger" 
                        size="sm" 
                        onClick={() => removeMedicineField(index)}
                        className="mb-3"
                      >
                        ×
                      </Button>
                    )}
                  </div>
                </div>
              </div>
            ))}

            <Button 
              variant="outline-primary" 
              size="sm" 
              type="button"
              onClick={addMedicineField}
              className="mb-3"
            >
              + Add Another Medicine
            </Button>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowNewPrescription(false)}>
              Cancel
            </Button>
            <Button variant="primary" type="submit">
              Save Prescription
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>

      {/* View Prescription Modal */}
      <Modal show={showViewModal} onHide={() => setShowViewModal(false)} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>Prescription Details</Modal.Title>
        </Modal.Header>
        {selectedPrescription && (
          <>
            <Modal.Body>
              <div className="mb-4">
                <div className="d-flex justify-content-between align-items-center mb-3">
                  <div>
                    <h4 className="mb-1">{selectedPrescription.patientName}</h4>
                    <p className="text-muted mb-0">
                      {selectedPrescription.patientAge} years, {selectedPrescription.patientGender}
                    </p>
                  </div>
                  <div className="text-end">
                    <div className="text-muted small">
                      <FiCalendar className="me-1" />
                      {new Date(selectedPrescription.createdAt).toLocaleDateString()}
                    </div>
                    <div className="text-muted small">
                      <FiClock className="me-1" />
                      {new Date(selectedPrescription.createdAt).toLocaleTimeString()}
                    </div>
                  </div>
                </div>

                <div className="mb-4">
                  <h6>Diagnosis</h6>
                  <p className="mb-0">{selectedPrescription.diagnosis}</p>
                </div>

                <div className="mb-3">
                  <h6>Medications</h6>
                  <Table bordered>
                    <thead>
                      <tr>
                        <th>Medicine</th>
                        <th>Dosage</th>
                        <th>Frequency</th>
                        <th>Duration</th>
                      </tr>
                    </thead>
                    <tbody>
                      {selectedPrescription.medicines.map((med, idx) => (
                        <tr key={idx}>
                          <td>{med.name}</td>
                          <td>{med.dosage}</td>
                          <td>{med.frequency}</td>
                          <td>{med.duration}</td>
                        </tr>
                      ))}
                    </tbody>
                  </Table>
                </div>

                {selectedPrescription.notes && (
                  <div className="alert alert-warning">
                    <FiAlertTriangle className="me-2" />
                    {selectedPrescription.notes}
                  </div>
                )}
              </div>
            </Modal.Body>
            <Modal.Footer>
              <Button variant="secondary" onClick={() => setShowViewModal(false)}>
                Close
              </Button>
              <Button variant="primary" onClick={() => window.print()}>
                <FiPrinter className="me-1" /> Print
              </Button>
            </Modal.Footer>
          </>
        )}
      </Modal>
    </div>
  );
};

export default Prescriptions;
