import React, { useState, useEffect } from 'react';
import { Table, Button, Badge, Form, InputGroup, Card, Alert } from 'react-bootstrap';
import { FiSearch, FiPlus, FiEdit2, FiTrash2, FiAlertTriangle } from 'react-icons/fi';

const Medicines = () => {
  const [medicines, setMedicines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [newMedicine, setNewMedicine] = useState({
    name: '',
    description: '',
    quantity: '',
    price: '',
    expiry_date: '',
    manufacturer: ''
  });

  // Mock data - replace with actual API call
  useEffect(() => {
    const fetchMedicines = async () => {
      try {
        // Simulate API call
        setTimeout(() => {
          const mockMedicines = [
            {
              id: 1,
              name: 'Amoxicillin 500mg',
              description: 'Antibiotic for bacterial infections',
              quantity: 150,
              price: 25.99,
              expiry_date: '2024-12-31',
              manufacturer: 'Pfizer',
              category: 'Antibiotic'
            },
            {
              id: 2,
              name: 'Ibuprofen 200mg',
              description: 'Pain reliever and anti-inflammatory',
              quantity: 320,
              price: 12.50,
              expiry_date: '2025-06-30',
              manufacturer: 'Johnson & Johnson',
              category: 'Pain Relief'
            },
          ];
          setMedicines(mockMedicines);
          setLoading(false);
        }, 1000);
      } catch (error) {
        console.error('Error fetching medicines:', error);
        setLoading(false);
      }
    };

    fetchMedicines();
  }, []);

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewMedicine({
      ...newMedicine,
      [name]: value
    });
  };

  const handleAddMedicine = (e) => {
    e.preventDefault();
    const newId = Math.max(...medicines.map(m => m.id), 0) + 1;
    const medicineToAdd = {
      ...newMedicine,
      id: newId,
      quantity: parseInt(newMedicine.quantity),
      price: parseFloat(newMedicine.price)
    };
    
    setMedicines([...medicines, medicineToAdd]);
    setNewMedicine({
      name: '',
      description: '',
      quantity: '',
      price: '',
      expiry_date: '',
      manufacturer: ''
    });
    setShowAddForm(false);
  };

  const handleDelete = (id) => {
    if (window.confirm('Are you sure you want to delete this medicine?')) {
      setMedicines(medicines.filter(medicine => medicine.id !== id));
    }
  };

  const filteredMedicines = medicines.filter(medicine =>
    medicine.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    medicine.description.toLowerCase().includes(searchTerm.toLowerCase())
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
    <div className="medicines">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Medicine Inventory</h2>
        <Button variant="primary" onClick={() => setShowAddForm(!showAddForm)}>
          <FiPlus className="me-1" /> Add New Medicine
        </Button>
      </div>

      {showAddForm && (
        <Card className="mb-4">
          <Card.Body>
            <h5 className="mb-4">Add New Medicine</h5>
            <Form onSubmit={handleAddMedicine}>
              <div className="row">
                <div className="col-md-6 mb-3">
                  <Form.Group>
                    <Form.Label>Medicine Name</Form.Label>
                    <Form.Control
                      type="text"
                      name="name"
                      value={newMedicine.name}
                      onChange={handleInputChange}
                      required
                    />
                  </Form.Group>
                </div>
                <div className="col-md-6 mb-3">
                  <Form.Group>
                    <Form.Label>Manufacturer</Form.Label>
                    <Form.Control
                      type="text"
                      name="manufacturer"
                      value={newMedicine.manufacturer}
                      onChange={handleInputChange}
                      required
                    />
                  </Form.Group>
                </div>
              </div>
              <div className="row">
                <div className="col-md-4 mb-3">
                  <Form.Group>
                    <Form.Label>Quantity</Form.Label>
                    <Form.Control
                      type="number"
                      name="quantity"
                      value={newMedicine.quantity}
                      onChange={handleInputChange}
                      required
                    />
                  </Form.Group>
                </div>
                <div className="col-md-4 mb-3">
                  <Form.Group>
                    <Form.Label>Price ($)</Form.Label>
                    <Form.Control
                      type="number"
                      step="0.01"
                      name="price"
                      value={newMedicine.price}
                      onChange={handleInputChange}
                      required
                    />
                  </Form.Group>
                </div>
                <div className="col-md-4 mb-3">
                  <Form.Group>
                    <Form.Label>Expiry Date</Form.Label>
                    <Form.Control
                      type="date"
                      name="expiry_date"
                      value={newMedicine.expiry_date}
                      onChange={handleInputChange}
                      required
                    />
                  </Form.Group>
                </div>
              </div>
              <Form.Group className="mb-3">
                <Form.Label>Description</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={2}
                  name="description"
                  value={newMedicine.description}
                  onChange={handleInputChange}
                />
              </Form.Group>
              <div className="d-flex justify-content-end gap-2">
                <Button variant="outline-secondary" onClick={() => setShowAddForm(false)}>
                  Cancel
                </Button>
                <Button variant="primary" type="submit">
                  Save Medicine
                </Button>
              </div>
            </Form>
          </Card.Body>
        </Card>
      )}

      <Card className="mb-4">
        <Card.Body>
          <div className="d-flex justify-content-between align-items-center mb-4">
            <h5 className="mb-0">All Medicines</h5>
            <div style={{ maxWidth: '300px' }}>
              <InputGroup>
                <InputGroup.Text>
                  <FiSearch />
                </InputGroup.Text>
                <Form.Control
                  type="text"
                  placeholder="Search medicines..."
                  value={searchTerm}
                  onChange={handleSearch}
                />
              </InputGroup>
            </div>
          </div>

          {filteredMedicines.length === 0 ? (
            <Alert variant="info">No medicines found. Add a new medicine to get started.</Alert>
          ) : (
            <div className="table-responsive">
              <Table hover className="align-middle">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Description</th>
                    <th className="text-end">Quantity</th>
                    <th className="text-end">Price</th>
                    <th>Expiry</th>
                    <th>Manufacturer</th>
                    <th className="text-end">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredMedicines.map((medicine) => (
                    <tr key={medicine.id}>
                      <td>
                        <div className="d-flex align-items-center">
                          {medicine.quantity < 20 && (
                            <FiAlertTriangle className="text-warning me-2" />
                          )}
                          {medicine.name}
                        </div>
                      </td>
                      <td className="text-muted">{medicine.description}</td>
                      <td className="text-end">
                        <Badge bg={medicine.quantity < 20 ? 'warning' : 'success'}>
                          {medicine.quantity} units
                        </Badge>
                      </td>
                      <td className="text-end">${medicine.price.toFixed(2)}</td>
                      <td>{new Date(medicine.expiry_date).toLocaleDateString()}</td>
                      <td>{medicine.manufacturer}</td>
                      <td className="text-end">
                        <Button variant="outline-primary" size="sm" className="me-2">
                          <FiEdit2 size={14} />
                        </Button>
                        <Button 
                          variant="outline-danger" 
                          size="sm"
                          onClick={() => handleDelete(medicine.id)}
                        >
                          <FiTrash2 size={14} />
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
    </div>
  );
};

export default Medicines;
